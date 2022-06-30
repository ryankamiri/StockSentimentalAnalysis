import helper
import finviz
from datetime import datetime
from pytz import timezone

MAX_DAYS = 3

data = []

for article in finviz.getScreener("v=341&s=ta_topgainers", 20):
    if (datetime.now(timezone('EST')) - article["date"]).days <= MAX_DAYS:
        #Write News
        data.append({"good_news": 1, "title": article["title"], "stock": article["ticker"], "date": str(article["date"]), "link": article["link"]})

for article in finviz.getScreener("v=341&s=n_majornews&f=ta_perf_dup&ft=4", 3):
    #Write News
    data.append({"good_news": 1, "title": article["title"], "stock": article["ticker"], "date": str(article["date"]), "link": article["link"]})

helper.writeData("gainers", data)

print(f"Successfully scraped {len(data)} Top Gainer News Headlines!")