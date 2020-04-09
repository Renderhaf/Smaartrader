import json
import requests
import sys

import InfoManager as IM

with open("./DataFiles/stockTickers.json", "r") as file:
    tickers = json.loads(file.read())

def getName(ticker:str)->str:
    return tickers.get(ticker, ticker)

def getWikiArticle(ticker: str)->str:
    name = getName(ticker)
    if name == ticker:
        quary = "Stock Market"
    else:
        quary = name
    url = 'https://en.wikipedia.org/w/api.php?action=opensearch&search="{}"&limit=1&format=json'.format(quary)
    return requests.get(url).json()[-1][0].replace("en.", "en.m.")

def getCurrentTrend(ticker: str, weeksBack:int=1):
    stockData = IM.getCandle(ticker, timeframe="Y", quality="high").get("c")
    priceDiff = stockData[-1] - stockData[-weeksBack*7]
    diffPrecentage = (priceDiff / stockData[-weeksBack*7]) * 100
    return round(diffPrecentage,3)

def main():
    print(getCurrentTrend("AAPL"))

if __name__ == "__main__":
    main()

