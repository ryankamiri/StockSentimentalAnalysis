import json
import newsfilter
from datetime import datetime

with open("./data/training_data.json", 'r') as f:
    datastore = json.load(f)

stocks = []

revData = datastore[::-1]

for i, data in enumerate(revData):
    if i < len(revData) - 1:
        nextStock = revData[i + 1]["stock"]
    else:
        nextStock = None
    if nextStock != data["stock"]:
        stocks.append({"ticker": data["stock"], "good_news": data["good_news"], "date": data["date"]})

newData = []
for i, info in enumerate(stocks):
    date = datetime.strptime(info["date"], "%Y-%m-%d %H:%M:%S%z")
    headlines = newsfilter.getNews([info["ticker"]])
    found = False
    for headline in headlines:
        if headline["date"].date() == date.date():
            newData.append({"good_news": info["good_news"], "title": headline["title"], "stock": headline["ticker"][0], "date": str(headline["date"]), "link": headline["link"]})
            found = True
        elif found:
            break
    print(f"{i + 1}/{len(stocks)}")

with open("./data/training_data_new.json", "w+", encoding="utf-8") as _file:
    _file.write(json.dumps(newData, indent=4))

print(f"Corpus decreased from {len(datastore)} to {len(newData)}.")