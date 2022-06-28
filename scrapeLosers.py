import helper
import finviz

data = []

for article in finviz.getScreener("v=341&s=ta_toplosers&f=cap_midover,sh_avgvol_o500,ta_perf_4wdown,ta_sma20_pb,ta_sma200_pb20&ft=3"):
    #Write News
    data.append({"good_news": 0, "title": article["title"], "stock": article["ticker"], "date": str(article["date"]), "link": article["link"]})

helper.writeData("losers", data)

print(f"Successfully scraped {len(data)} Top Loser News Headlines!")