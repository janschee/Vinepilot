import os
import yaml
import logging

class Project():
    #Paths
    this_file: str = os.path.abspath(__file__)
    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))
    config_file: str = os.path.normpath(os.path.join(base_dir, "./vinepilot/config/config.yaml")) 
    config: dict = yaml.safe_load(open(config_file, "r"))
    image_dir: str = os.path.normpath(os.path.join(base_dir, config["project"]["image_dir"]))
    data_path: str = os.path.normpath(os.path.join(base_dir, config["project"]["data"]))
    vineyards_dir: str = os.path.normpath(os.path.join(base_dir, config["project"]["vineyards_dir"]))
    model_dir: str = os.path.normpath(os.path.join(base_dir, config["project"]["model_dir"]))

    #Train
    batch_size: int = config["train"]["batch_size"]
    epochs: int = config["train"]["epochs"]
    shuffle: bool = config["train"]["shuffle"]
    learning_rate: float = config["train"]["learning_rate"]
    optimizer: str = config["train"]["optimizer"]
    loss: str = config["train"]["loss"]

    #Logging
    levels: dict = {"debug": logging.DEBUG, "info": logging.INFO, "warning": logging.WARNING, "error": logging.ERROR, "critical": logging.CRITICAL}
    logging_level = config["runtime"]["logging_level"]
    assert logging_level in levels.keys(), f"Unknown logging level in config file! Choose from {list(levels.keys())}!"
    logging.basicConfig(level=levels[logging_level])

    #Server
    host_address: str = config["server"]["host_address"]
    port: int = config["server"]["port"]
