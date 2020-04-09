import json
import requests
import sys

import InfoManager as IM


def getWikiArticle(ticker: str)->str:
    '''
    returns a wikipedia article about the stock ticker. If it cant find a article, it gives an article about the stock market
    '''
    name = IM.getName(ticker)
    defaultArticle = "https://en.m.wikipedia.org/wiki/Stock_market"
    if name == ticker:
        return defaultArticle
    else:
        quary = name
    url = 'https://en.wikipedia.org/w/api.php?action=opensearch&search="{}"&limit=1&format=json'.format(quary)

    try:
        wikilink = requests.get(url).json()[-1][0].replace("en.", "en.m.")
    except IndexError:
        return defaultArticle
    return wikilink

def getCurrentTrend(ticker: str, weeksBack:int=1):
    stockData = IM.getCandle(ticker, timeframe="Y", quality="high").get("c")
    priceDiff = stockData[-1] - stockData[-weeksBack*7]
    diffPrecentage = (priceDiff / stockData[-weeksBack*7]) * 100
    return round(diffPrecentage,3)

def main():
    print(getCurrentTrend("AAPL"))

if __name__ == "__main__":
    main()

