
"""
This script generates a markdown file based on the data from data.csv.
The markdown file contains a dataset overview and displays the images.
"""
import sys

#Get path to data.csv
path = sys.argv[1]

#Dataloader
def load(file):
    for line in file: yield line

#Generate Markdown
md = "# WineRover Dataset\n"
md += "## Dataset Images\n"
with open(path, 'r') as data:
    read_line = load(data)
    next(read_line) #Skip csv header
    for i, line in enumerate(read_line):
        line = line[:-1] #Remove line break
        md += f"![Image_{str(i).zfill(4)}]({line})\n"

#Dump File
with open("./dataset_overview.md", 'w') as md_file: md_file.write(md)



