
"""
This script downloads the images listed in data.csv
"""
import requests
import shutil
import json
import yaml
import os

target_dir = "./imgs"
this_file: str = os.path.abspath(__file__)
base_dir: str = os.path.dirname(os.path.dirname(this_file))
config_file: str = os.path.normpath(os.path.join(base_dir, "./config.yaml")) 
config: dict = yaml.safe_load(open(config_file, "r"))
data_path: str = os.path.normpath(os.path.join(base_dir, config["dataset"]["data"]))
data: list[dict] = json.load(open(data_path, "r"))

for sample in data:
    image_id: int = int(sample["id"])
    url: str = sample["data"]["ImageURL"]
    img_req = requests.get(url,stream=True)
    if img_req.status_code == 200:
        print(f"Get image {image_id}")
        img_req.decode_content = True
        with open(f"{target_dir}/img_{str(image_id).zfill(4)}.jpg", 'wb') as f: shutil.copyfileobj(img_req.raw,f)
    else:
        print(f"Failed to get image {image_id}")
        break



       



