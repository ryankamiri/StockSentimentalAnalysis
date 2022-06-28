import requests
from bs4 import BeautifulSoup

url = "https://www.marketwatch.com/"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
headlines = soup.find('body').find_all('h3')

f = open('output.txt','a')
for x in headlines:
    f.write(x.text.strip() + '\n')

f.close()