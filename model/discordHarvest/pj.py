import requests
from datetime import datetime, timedelta
from pytz import timezone
from dotenv import load_dotenv
import json
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import newsfilter

#Top Positive News Movers Permarket from Atlas Trading Discord. Mostly positive

load_dotenv()

SEARCH_URL = "https://discord.com/api/v9/guilds/428232997737594901/messages/search?author_id=332561722621820951&content=Top%20positive"


total = None

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    "authorization": os.getenv("DISCORD_TOKEN")
}

stocks = []
total = 0
done = 0

while True:
    r = requests.get(f"{SEARCH_URL}&offset={done}", headers=headers)
    if r.status_code != 200:
        print(f"{r.status_code} Error: {r.text}")
        break

    info = r.json()
    total = info["total_results"]
    
    for message in info["messages"]:
        message = message[0]
        content = message["content"].replace("Top Positive News Movers Premarket: \n\n", "").replace("```", "").split("\n")
        date = message["timestamp"]
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")

        for line in content:
            idx = line.find(" ")
            stock = line[:idx].replace(":", "").strip()
            if not stock.isupper():
                continue
            reason = line[idx:].lower()
            if "+" in reason:
                sentiment = 1
            elif "-" in reason:
                sentiment = 0
            else:
                continue
            
            if "earnings" in reason:
                continue
            elif "momentum mover" in reason:
                continue

            stocks.append({"ticker": stock, "reason": reason, "good_news": sentiment, "date": date})

    done += len(info["messages"])
    if done == total:
        break

print(f"Aquired {len(stocks)} stocks.")

newData = []

for i, info in enumerate(stocks):
    date = info["date"]
    preMarketStart = datetime(date.year, date.month, date.day, 4, 0, 0, tzinfo=timezone("US/Eastern"))
    # yesterday = date - timedelta(days=1)
    # marketEnd = datetime(yesterday.year, yesterday.month, yesterday.day, 16, 0, 0, tzinfo=timezone("US/Eastern"))
    preMarketEnd = datetime(date.year, date.month, date.day, 9, 30, 0, tzinfo=timezone("US/Eastern"))
    headlines = newsfilter.getNews([info["ticker"]])
    found = False
    for headline in headlines:
        if preMarketStart <= headline["date"] <= preMarketEnd:
            newData.append({"good_news": info["good_news"], "title": headline["title"], "stock": headline["ticker"], "date": str(headline["date"]), "link": headline["link"]})
            found = True
        elif found:
            break
    print(f"{i + 1}/{len(stocks)}")

with open("../data/training_data_pj.json", "w+", encoding="utf-8") as _file:
    _file.write(json.dumps(newData, indent=4))

print(f"Created Corpus of {len(newData)}.")