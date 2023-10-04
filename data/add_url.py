

"""
This program takes one url-string as an agrument.
It checks wether the url is already in the dataset.
If it is, it will report this.
If not, it will add the url to the dataset.
"""
import sys
import datetime
import json
import copy

if __name__ == "__main__":
    file_path = sys.argv[1]
    with open(file_path,'r') as file: dataset = list(json.load(file))
    list_of_urls = [sample["data"]["ImageURL"] for sample in dataset]
    new_urls = []

    print("Welcome to the dataset wizard!")
    url_input: str = "notEmpty"

    while url_input != "":
        url_input: str = str(input("Enter URL or save file (save):"))
        url = url_input.strip()

        #Save data
        if url == "save":
            with open("base.json", "r") as base: base_json = json.load(base)
            for idx, url in enumerate(new_urls):
                sample_json = copy.deepcopy(base_json)
                sample_json["data"]["ImageURL"] = url
                sample_json["id"] = idx + len(list_of_urls) + 1
                dataset.append(sample_json)

            with open(f"{datetime.datetime.now()}.json", "w") as target:
                json.dump(dataset, target, indent=4)

            break
        
        #Check URL
        if url in list_of_urls or url in new_urls:
            print("URL does already exist!")
        else:
            print("Add URL to dataset!")
            new_urls.append(url)
