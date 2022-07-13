import json
import helper
import os

files = [helper.findFilename("gainers", "data"), helper.findFilename("losers", "data")]

newData = []
data = []
added = 0
dataFilename = "data/training_data.json"

for filename in files:
    with open(f"data/{filename}", "r", encoding="utf-8") as _file:
        newData += json.load(_file)

if not os.path.exists(dataFilename):
    with open(dataFilename, "w+", encoding="utf-8") as _file:
        _file.write([])

with open(dataFilename, "r", encoding="utf-8") as _file:
    data = json.load(_file)

for article in newData:
    if not helper.articleExists(data, article):
        data.append(article)
        added += 1

with open(dataFilename, "w+", encoding="utf-8") as _file:
    _file.write(json.dumps(data, indent=4))

print(f"Added {added} new articles. You now have {len(data)} training articles.")