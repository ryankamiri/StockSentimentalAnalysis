import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import json

MAX_DAYS = 3

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
}

data = []

for page in range(20):
    url = f"https://finviz.com/screener.ashx?v=341&s=ta_topgainers&r={page}1"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"{r.status_code} Error: {r.text}")
        continue
    soup = BeautifulSoup(r.text, 'html.parser')
    elements = soup.find("table", {"id": "screener-views-table"}).findAll("tr", recursive=False)

    idx = 4
    while idx < len(elements) - 2:
        ticker = elements[idx].find("a", {"class": "tab-link"})
        if not ticker:
            idx += 1
            continue
        ticker = ticker.text
        idx += 1
        news = elements[idx].find("table", {"class": "body-table-news"})
        if not news:
            idx += 1
            continue
        news = news.findAll("tr", recursive=False)
        for article in news:
            date = article.findAll("td")[0].text
            temp = article.find("a", {"class": "tab-link-news"})
            title = temp.text
            link = temp.attrs["href"]

            date = datetime.strptime(date, "%b-%d-%y %I:%M%p").replace(tzinfo=timezone('EST'))

            if (datetime.now(timezone('EST')) - date).days <= MAX_DAYS:
                #Write News
                data.append({"good_news": 1, "title": title, "stock": ticker, "date": str(date), "link": link})
        idx += 1

with open("gainers.json", "w+", encoding="utf-8") as _file:
    _file.write(json.dumps(data, indent=4))

print(f"Successfully scraped {len(data)} Top Gainer News Headlines!")