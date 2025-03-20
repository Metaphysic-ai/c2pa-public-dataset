import os
import mimetypes
import logging
from io import BytesIO

from c2pa import Builder, SigningAlg, create_signer, c2pa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.hazmat.primitives.asymmetric import ec

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TIMESTAMP_URL = "http://timestamp.digicert.com"


class C2paSign:
    def __init__(self, title, assertions):
        with open("../certs/es256_private.key", "rb") as f:
            private_key = f.read()

        with open("../certs/es256_certs.pem", "rb") as f:
            public_certs = f.read()

        def sign_ps256_callback(data):
            return self.sign_ps256(data, private_key)

        self.manifest_store = {
            "claim_generator_info": [{
                "name": "Metaphysic PRO",
            }],
            "title": title,
            "assertions": assertions,
            "ingredients": [],
        }

        self.signer = create_signer(sign_ps256_callback, SigningAlg.ES256, public_certs, TIMESTAMP_URL)

    def sign_files(self, partition_files: dict):
        total_size_mb = []

        for partition_type, files in partition_files.items():
            for file in files:
                file_path = file["file_path"]
                file_size_mb = os.path.getsize(file_path) >> 20
                total_size_mb.append(file_size_mb)

        self.manifest_store["assertions"].append({
            "label": "metaphysic.composition",
            "data": {
                "size": f"{len(total_size_mb)} files, {sum(total_size_mb)}Mb",
                "split": "The dataset is split into three files - training, evaluation, and test.",
                "features": "Video files with 1920 x 1080 resolution, AAC HEVC codecs, HD colour profile (1-1-1), stereo audio channels, in MOV format.",
            },
        })

        sign_files = []
        ingredients = []
        builder = Builder(self.manifest_store)
        for partition_type, files in partition_files.items():
            metadata = {
                "partitionType": partition_type,
                "assets": [],
            }

            for file in files:
                file_path = file["file_path"]
                ingredient_label = file["ingredient_label"]

                metadata["assets"].append({
                    "path": file_path,
                    "size_mb": file_size_mb,
                })

                mime_type, _ = mimetypes.guess_type(file_path, strict=False)
                if mime_type is None:
                    mime_type = "application/octet-stream"
                elif mime_type == "audio/mp3":
                    mime_type = "audio/mpeg"

                ingredient = {
                    "title": ingredient_label,
                    "relationship": "parentOf",
                    "description": partition_type,
                    "format": mime_type,
                }

                logger.info(f"Adding ingredient file ={file_path} to the manifest.")

                ingredient_bytes = BytesIO()
                with open(file_path, "rb") as file_handler:
                    try:
                        builder.sign(self.signer, mime_type, file_handler, ingredient_bytes)
                    except c2pa.c2pa.Error.NotSupported as e:
                        logger.warning(f"File {file_path} type {mime_type} not supported.")
                        continue

                ingredients.append((ingredient, mime_type, ingredient_bytes))
                sign_files.append(file_path)

        logger.info("Adding ingredients.")
        for ingredient, mime_type, ingredient_bytes in ingredients:
            builder.add_ingredient(ingredient, mime_type, ingredient_bytes)

        for file_path in sign_files:
            filename, file_extension = os.path.splitext(file_path)
            output_path = f"{filename}_signed{file_extension}"

            logger.info(f"Signing {file_path} type {mime_type} to {output_path}")

            if os.path.exists(output_path):
                os.remove(output_path)

            builder.sign_file(self.signer, file_path, output_path)
            logger.info(f"File = {filename} sucessfully signed.")

    @staticmethod
    def sign_ps256(data, private_key_data):
        private_key = serialization.load_pem_private_key(
            private_key_data,
            password=None,
        )
        digest = hashes.Hash(hashes.SHA256())
        digest.update(data)
        hashed_data = digest.finalize()

        signature = private_key.sign(
            hashed_data,
            ec.ECDSA(Prehashed(hashes.SHA256()))
        )
        return signature
