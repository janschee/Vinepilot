import json
import copy

new_json: list = []
base_json = json.load(open("base.json", "r"))
with open("data.json",) as old_file:
    old_json = json.load(old_file)
    for sample in old_json:
        idx = sample["id"]
        url = sample["data"]["ImageURL"]
        results: list = sample["annotations"][0]["result"]


        new_sample = copy.deepcopy(base_json)
        new_sample["id"] = idx
        new_sample["data"]["ImageURL"] = url

        if len(results) == 2:
            points = results[1]["value"]["points"]
            new_sample["annotations"][0]["result"][1]["value"]["points"] = points


        new_json.append(new_sample)
    
with open("newdata.json", "w") as new_file:
    json.dump(new_json, new_file, indent=4)

