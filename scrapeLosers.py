import helper
import finviz
from datetime import datetime
from pytz import timezone

MAX_DAYS = 3

data = []

for article in finviz.getScreener("v=341&s=ta_toplosers&f=cap_midover,sh_avgvol_o500,ta_perf_4wdown,ta_sma20_pb,ta_sma200_pb20&ft=3", 2):
    #Write News
    data.append({"good_news": 0, "title": article["title"], "stock": article["ticker"], "date": str(article["date"]), "link": article["link"]})


for article in finviz.getScreener("v=341&s=n_majornews&f=cap_midunder,ta_perf_ddown&ft=4", 3):
    #Write News
    data.append({"good_news": 0, "title": article["title"], "stock": article["ticker"], "date": str(article["date"]), "link": article["link"]})

for article in finviz.getScreener("v=341&s=ta_newlow&f=sh_price_o5&ft=4", 5):
    if (datetime.now(timezone('EST')) - article["date"]).days <= MAX_DAYS:
        #Write News
        data.append({"good_news": 0, "title": article["title"], "stock": article["ticker"], "date": str(article["date"]), "link": article["link"]})

for article in finviz.getScreener("v=341&s=ta_newlow&f=sh_avgvol_o500,ta_perf_1w10u&ft=4", 10):
    if (datetime.now(timezone('EST')) - article["date"]).days <= MAX_DAYS:
        #Write News
        data.append({"good_news": 0, "title": article["title"], "stock": article["ticker"], "date": str(article["date"]), "link": article["link"]})


helper.writeData("losers", data)

print(f"Successfully scraped {len(data)} Top Loser News Headlines!")