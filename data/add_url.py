

"""
This program takes one url-string as an agrument.
It checks wether the url is already in the dataset.
If it is, it will report this.
If not, it will add the url to the dataset.
"""

import sys

url = sys.argv[1]
with open("./data.csv",'r') as file: dataset = [line for line in file]



