import c2pa
import json
import logging
import argparse

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class C2PAExtractor:
    def c2pa_data_from_file(self, file_path: str):
        logger.info(f"Extracting data from {file_path}")
        try:
            return json.loads(c2pa.Reader.from_file(file_path).json())
        except Exception as e:
            logger.warning(f"File = {file_path} appears to have no manifest: {e}")
            return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract C2PA metadata from a file.")
    parser.add_argument("file_path", type=str, help="Path to the file to extract C2PA data from")
    args = parser.parse_args()

    extractor = C2PAExtractor()
    metadata = extractor.c2pa_data_from_file(args.file_path)

    if metadata:
        print(json.dumps(metadata, indent=4, ensure_ascii=False))
    else:
        logger.error("No metadata found.")
