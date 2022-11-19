import requests
from bs4 import BeautifulSoup

def scraping_v1(url):
  data={}
  url = url

  payload = ""
  headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
  }

  response = requests.request("POST", url, headers=headers, data=payload,timeout=10)

  soup=BeautifulSoup(response.text,"html.parser")
  titulo=soup.title.text
  h2_group=soup.find_all("h2")
  imagen=soup.find('img').attrs["src"]
  #print(imagen)
  #if have a \n or \r invoke .strip()
  subtitles= [titles_h2.text for titles_h2 in h2_group ]
  data["title"]=titulo
  data["subtitles"]=subtitles
  data["img"]=imagen
  return data


print(scraping_v1("https://www.benzinga.com/markets/cryptocurrency/22/09/28858937/bitcoin-ethereum-dogecoin-plunge-sharply-after-hot-inflation-repot-analyst-says-apex-coin-"))
