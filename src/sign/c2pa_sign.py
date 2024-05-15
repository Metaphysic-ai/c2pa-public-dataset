import os
import json

import c2pa


class C2paSign:
    def __init__(self, title, assertions):
        self.public_certs = open("../certs/es256_certs.pem", "rb").read()
        self.private_key = open("../certs/es256_private.key", "rb").read()

        manifest_store = {
            "claim_generator": "Metaphysic",
            "title": title,
            "assertions": assertions,
            "ingredients": [],
        }

        self.manifest_store = manifest_store

    def sign_files(self, partition_files: dict, manifests_dir=None):
        total_size_mb = []

        for partition_type, files in partition_files.items():
            print (f"Signing {len(files)} files for {partition_type}")

            metadata = {
                "partitionType": partition_type,
                "assets": [],
            }

            for file_path, manifest_path, manifest_label in files:
                file_size_mb = os.path.getsize(file_path) >> 20
                total_size_mb.append(file_size_mb)

                metadata["assets"].append({
                    "path": file_path,
                    "size_mb": file_size_mb,
                })

                ingredient = {
                    "title": manifest_label,
                    "relationship": "componentOf",
                    "metadata": metadata,
                    "description": partition_type,
                    "active_manifest": manifest_label,
                }
                if manifest_path:
                    ingredient["manifest_data"] = {
                        "format": "application/c2pa",
                        "identifier": manifest_path,
                    }
                self.manifest_store["ingredients"].append(ingredient)

        self.manifest_store["assertions"].append({
            "label": "metaphysic.composition",
            "data": {
                "size": f"{len(total_size_mb)} files, {sum(total_size_mb)}Mb",
                "split": "The dataset is split into three files - training, evaluation, and test.",
                "features": "Video files with 1920 x 1080 resolution, AAC HEVC codecs, HD colour profile (1-1-1), stereo audio channels, in MOV format.",
            },
        })

        sign_info = c2pa.SignerInfo("es256", self.public_certs, self.private_key, "http://timestamp.digicert.com")

        for files in partition_files.values():
            for file_path, _, _ in files:
                filename, file_extension = os.path.splitext(file_path)
                destination_file = f"{filename}_signed{file_extension}"

                c2pa.sign_file(
                    file_path,
                    destination_file,
                    json.dumps(self.manifest_store),
                    sign_info,
                    data_dir=manifests_dir,
                )
