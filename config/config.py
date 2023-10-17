import os
import yaml

class Project():
    this_file: str = os.path.abspath(__file__)
    base_dir: str = os.path.dirname(os.path.dirname(this_file))
    config_file: str = os.path.normpath(os.path.join(base_dir, "./config/config.yaml")) 
    config: dict = yaml.safe_load(open(config_file, "r"))
    image_dir: str = os.path.normpath(os.path.join(base_dir, config["dataset"]["image_dir"]))
    data_path: str = os.path.normpath(os.path.join(base_dir, config["dataset"]["data"]))

if __name__ == "__main__":
    print(__package__)