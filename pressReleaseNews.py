from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import json

url = "https://www.nasdaq.com/market-activity/quotes/press-releases/"

r = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
data=r.text
soup = BeautifulSoup(data, 'html.parser')
get_table = soup.find("table", attrs={'class':'tablefield'})

get_table_data = get_table.tbody.find_all("td")
# print(get_table_data[0].find("a"))

stock_urls = []
for i in range(len(get_table_data)):
    stock_urls.append(get_table_data[i].find("a", href=True).find("u").text.lower())
#print(stock_urls)

dates = []
headlines = []
stock = []

for j in range(0, len(stock_urls), 2):
    url = "https://api.nasdaq.com/api/news/topic/press_release?q=symbol:" + stock_urls[j] +"%7Cassetclass:stocks&limit=4&offset=0"
    r = requests.get(url, headers={'Accept': 'application/xml; charset=utf-8','User-Agent':'foo'})
    data = r.json()
    for x in range(len(data['data']['rows'])):
        headlines.append(data['data']['rows'][x]['title'])
        dates.append(data['data']['rows'][x]['created'])
        stock.append(stock_urls[j])

# displaying the info
for i in range(len(stock)):
    print(stock[i], dates[i], headlines[i])