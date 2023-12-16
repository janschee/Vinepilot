import sys
import yaml
import gdown

#Read yaml
path: str = str(sys.argv[1])
with open(path, "r") as yaml_file:
    data: dict = yaml.safe_load(yaml_file)

#Get google drive url
file_name: str = data["gdown"]["file_name"]
file_url: str = data["gdown"]["file_url"]

#Download
gdown.download(url=file_url, output=file_name, quiet=False, fuzzy=True)

