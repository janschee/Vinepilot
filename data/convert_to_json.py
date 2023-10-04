import sys
import json
import copy

csv_data = sys.argv[1]
new_json = []
with open("base.json", "r") as base: base_json = json.load(base)

with open(csv_data, 'r') as source:
    for idx, url in enumerate(source):
        sample_json = copy.deepcopy(base_json)
        sample_json["data"]["ImageURL"] = url[:-1]
        sample_json["id"] = idx + 1
        new_json.append(sample_json)

with open("data.json", "w") as target:
    json.dump(new_json, target, indent=4)

