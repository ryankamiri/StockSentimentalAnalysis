# With key issues found with training data,
# we decided to fix the data with this script.
# This script will run through negative headlines
# and the user will attempt to identify false
# bearish headlines and they will be disregarded.

import json
import os

with open("./data/training_data.json", 'r') as f:
    datastore = json.load(f)

data = []
stop = False

for idx, item in enumerate(datastore):
    os.system("cls")
    if stop:
        data += datastore[idx:]
        break
    headline = item['title']
    label = item['good_news']
    if label == 0:
        print(f"{idx + 1}/{len(datastore)}")
        print(f"SHOULD THE HEADLINE BE DISREGARDED?")
        print(headline)
        response = str(input()).lower()
        if response == "1" or response == "y":
            #Remove from dataset
            print("REMOVED HEADLINE")
            continue
        elif response == "stop":
            stop = True
    data.append(item)

with open("./data/training_data_fixed.json", "w+", encoding="utf-8") as _file:
    _file.write(json.dumps(data, indent=4))

print(f"Corpus decreased from {len(datastore)} to {len(data)}.")