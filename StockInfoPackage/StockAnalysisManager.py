import json
import requests
import sys
import matplotlib.pyplot as plt

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
    '''
    returns the current trend for @param weeksBack in precentage
    '''
    stockData = IM.getCandle(ticker, timeframe="Y", quality="high").get("c")
    priceDiff = stockData[-1] - stockData[-weeksBack*7]
    diffPrecentage = (priceDiff / stockData[-weeksBack*7]) * 100
    return round(diffPrecentage,3)

def getHistoricSMA(ticker: str, sampleSize: int=25):
    '''
    returns a list of a simple moving avarage (equal weighted)

    * The list used should be shifted forward @param sampleSize times, since SMA is not calculated for those
    '''
    stockData = IM.getCandle(ticker, timeframe="Y", quality="high").get("c")
    sma = []
    for i in range(0, len(stockData)-sampleSize):
        sma.append(sum(stockData[i : i + sampleSize])/sampleSize)
    return sma

def getCurrentSMA(ticker: str, sampleSize: int=25, returnPrice: bool=False):
    '''
    returns the current simple avarage with @param sampleSize days

    * if @param returnPrice is true, this will return a tuple containing the SMA and the current price (mostly used for comparison)
    '''
    stockData = IM.getCandle(ticker, timeframe="Y", quality="high").get("c")[-sampleSize-1:]
    sma = 0
    for i in range(0, len(stockData)-sampleSize):
        sma = (sum(stockData[i : i + sampleSize])/sampleSize)
    
    if returnPrice:
        return round(sma,2), stockData[-1]
    else:
        return round(sma,2)

def getHistoricEMA(ticker: str, sampleSize: int=25, returnPrice: bool=False):
    '''
    returns a list of a exponential moving avarage (equal weighted)

    * The list used should be shifted forward @param sampleSize times, since EMA is not calculated for those
    * if @param returnPrice is true, this will return a tuple containing the SMA and the current price (mostly used for comparison)
    '''
    stockData = IM.getCandle(ticker, timeframe="Y", quality="high").get("c")
    mult = 2 / (sampleSize+1)
    ema = []
    for i in range(sampleSize-1, len(stockData)):
        if len(ema) == 0:
            # Calculate inital SMA value
            ema.append(sum(stockData[i - sampleSize + 1: i]) / sampleSize)
        else:
            # Calculate todays EMA, based on yesterdays EMA
            ema.append( ((stockData[i]-ema[len(ema)-1]) * mult) + ema[len(ema)-1])

    if returnPrice:
        return ema, stockData[-1]
    return ema

def getCurrentEMA(ticker: str, sampleSize: int=20, returnPrice: bool=False):
    '''
    returns the current exponential avarage with @param sampleSize days
    
    * if @param returnPrice is true, this will return a tuple containing the EMA and the current price (mostly used for comparison)
    '''

    if returnPrice:
        return round(getHistoricEMA(ticker, sampleSize, True)[-1],2)
    return round(getHistoricEMA(ticker, sampleSize)[-1],2)

def test():
    ticker = 'AAPL'
    normalStockY = IM.getCandle(ticker, timeframe="Y", quality="high").get("c")
    normalStockX = [x for x in range(len(normalStockY))]

    sampleSize = 30
    smaY = getHistoricSMA(ticker, sampleSize)
    smaX = [x + sampleSize for x in range(len(smaY))]

    emaY = getHistoricEMA(ticker, sampleSize)
    emaX = [x + sampleSize for x in range(len(emaY))]

    plt.plot(normalStockX, normalStockY)
    plt.plot(smaX, smaY)
    plt.plot(emaX, emaY)
    print(getCurrentEMA("AAPL", sampleSize), emaY[-1])
    plt.show()

if __name__ == "__main__":
    test()

