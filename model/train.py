
import json

from model import TrackDetectionModel

config: dict = json.load(open("./config.json", "r"))


def load_sample() -> tuple: #(data, annotations)
    with open(config["train"]["train_data"], "r") as f:
        train_data = json.load(f)
        for sample in train_data:
            image_id: int = sample["id"]
            annotations: list = sample["annotations"][0]["result"][1]#["value"]["points"]

            print(image_id, annotations)

if __name__ == "__main__":
    load_sample()
        
