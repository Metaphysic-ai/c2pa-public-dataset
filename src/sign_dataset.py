import os
import json

from sign.c2pa_sign import C2paSign


class C2paDataset:
    def __init__(self):
        title = "Metaphysic Test Dataset for C2PA"

        with open("../sample/dataset_demo_assertions.json", "r") as f:
            assertions = json.loads(f.read())

        data_dir = "../sample"

        partition_files = {
            "training": [
                (
                    f"{data_dir}/training/Metaphysic C2PA training partition dataset.mp4",
                    "training/Metaphysic C2PA training partition dataset.c2pa",
                    "metaphysic.training_dataset"
                ),
            ],
            "test": [
                (
                    f"{data_dir}/test/Metaphysic C2PA test partition dataset.mp4",
                    "test/Metaphysic C2PA test partition dataset.c2pa",
                    "metaphysic.test_dataset"
                ),
            ],
            "evaluation": [
                (
                    f"{data_dir}/evaluation/Metaphysic C2PA evaluation partition dataset.mp4",
                    "evaluation/Metaphysic C2PA evaluation partition dataset.c2pa",
                    "metaphysic.evaluation_dataset"
                ),
            ],
            "AIML-training-dataset-hierarchical": [
                (
                    f"{data_dir}/AIML-training-dataset-hierarchical.cddl",
                    None,
                    "metaphysic.AIML-training-dataset-hierarchical"
                ),
            ],
        }

        c2pa_sign = C2paSign(title, assertions)
        c2pa_sign.sign_files(partition_files, manifests_dir=data_dir)

if __name__ == '__main__':
    C2paDataset()
