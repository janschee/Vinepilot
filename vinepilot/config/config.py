import os
import yaml

class Project():
    #Paths
    this_file: str = os.path.abspath(__file__)
    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))
    config_file: str = os.path.normpath(os.path.join(base_dir, "./vinepilot/config/config.yaml")) 
    config: dict = yaml.safe_load(open(config_file, "r"))
    image_dir: str = os.path.normpath(os.path.join(base_dir, config["dataset"]["image_dir"]))
    data_path: str = os.path.normpath(os.path.join(base_dir, config["dataset"]["data"]))

    #Configs
    batch_size: int = config["train"]["batch_size"]
    shuffle: bool = config["train"]["shuffle"]

