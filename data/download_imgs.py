
"""
This script downloads the images listed in data.csv
"""
import sys
import requests
import shutil

#Get paths
path = sys.argv[1]
target_dir = "./imgs"

#Dataloader
def load(file):
    for line in file: yield line

#Pull images
with open(path, 'r') as data:
    read_line = load(data)
    next(read_line) #Skip csv header
    for i, url in enumerate(read_line):
        url = url[:-1] #Remove line break
        img_req = requests.get(url,stream=True)
        if img_req.status_code == 200:
            print(f"Get image {i}")
            img_req.decode_content = True
            with open(f"{target_dir}/img_{str(i).zfill(4)}.jpg", 'wb') as f: shutil.copyfileobj(img_req.raw,f)
        else:
            print(f"Failed to get image {i}")
            break



       



