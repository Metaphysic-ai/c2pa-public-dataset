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
                {
                    "file_path": f"{data_dir}/training/Metaphysic C2PA training partition dataset.mp4",
                    "ingredient_label": "metaphysic.training_dataset",
                },
            ],
            "test": [
                {
                    "file_path": f"{data_dir}/test/Metaphysic C2PA test partition dataset.mp4",
                    "ingredient_label": "metaphysic.test_dataset",
                },
            ],
            "evaluation": [
                {
                    "file_path": f"{data_dir}/evaluation/Metaphysic C2PA evaluation partition dataset.mp4",
                    "ingredient_label": "metaphysic.evaluation_dataset",
                },
            ],
            "AIML-training-dataset-hierarchical": [
                {
                    "file_path": f"{data_dir}/AIML-training-dataset-hierarchical.cddl",
                    "ingredient_label": "metaphysic.AIML-training-dataset-hierarchical"
                },
            ],
        }

        c2pa_sign = C2paSign(title, assertions)
        c2pa_sign.sign_files(partition_files)

if __name__ == '__main__':
    C2paDataset()
