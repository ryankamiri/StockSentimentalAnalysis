import requests
from datetime import datetime
from pytz import timezone

URL = "https://api.newsfilter.io/public/actions"
SOURCES = "(source.id:sec-api OR source.id:analystUpgrades OR source.id:secPressReleases OR source.id:clinicalTrials OR source.id:usFda OR source.id:usSam OR source.id:uspto OR source.id:fcc OR source.id:prNewswire OR source.id:usptoTrialAndAppeal OR source.id:usDod OR source.id:usEconomicIndicators OR source.id:earningsCallTranscripts OR source.id:businesswire OR source.id:globenewswire)"

def getHeaders():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        "caching-key": "sfksmdmdg0aadsf224533130"
    }
    return headers

def getNews(symbols=[], offset=0, limit=50):
    if symbols == []:
        query = SOURCES
    else:
        query = f"symbols:{','.join(symbols)} AND {SOURCES}"
    data = {
        "type": "filterArticles",
        "isPublic": True,
        "queryString": query,
        "from": offset,
        "size": limit
    }

    headers = getHeaders()
    r = requests.post(URL, headers=headers, json=data)
    if r.status_code != 200:
        print(f"{r.status_code} Error: {r.text}")
        return []
    dataStore = []
    for article in r.json()["articles"]:
        date = article["publishedAt"]
        try:
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone('UTC'))
        except:
            try:
                date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone('UTC'))
            except:
                date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
        dataStore.append({"title": article["title"], "ticker": article["symbols"], "date": date, "link": article["url"]})
    
    return dataStore
    