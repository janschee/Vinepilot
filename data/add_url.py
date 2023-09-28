

"""
This program takes one url-string as an agrument.
It checks wether the url is already in the dataset.
If it is, it will report this.
If not, it will add the url to the dataset.
"""
import sys
import datetime

if __name__ == "__main__":
    file_path = sys.argv[1]
    with open(file_path,'r') as file: dataset: list = [line[:-1] for line in file]

    print("Welcome to the dataset wizard!")
    url_input: str = "notEmpty"

    while url_input != "":
        url_input: str = str(input("Enter URL or save file (save):"))
        url = url_input.strip()

        #Save data
        if url == "save":
            data = ""
            for line in dataset:
                data += str(line)
                data += "\n"
            with open(str(f"data_{str(datetime.datetime.now())}").replace(" ","_") + ".csv", "w") as f:
                f.write(data)
            break
        
        #Check URL
        if url in dataset:
            print("URL does already exist!")
        else:
            print("Add URL to dataset!")
            dataset.append(url)