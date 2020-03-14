import requests
import json
import time
import matplotlib.pyplot as plt
import numpy as np

class StockManager():
    def __init__(self):
        with open("APIKEYS.json", "r") as file:
            data = json.loads(file.read())
            key = data["Finnhub"]
        self.request = "https://finnhub.io/api/v1/{}?{}&token=" + key
    
    def getRawQuote(self, symbol) -> dict:
        req = requests.get(self.request.format('quote','symbol='+symbol))
        return req.json()


    def getQuote(self,symbol):
        req = self.getRawQuote(symbol)
        fixedDict=dict()
        fixedDict["stockSymbol"]=symbol
        fixedDict['current_price']=req['c']
        fixedDict['today_high']=req['h']
        fixedDict['today_low']=req['l']
        fixedDict['open_price']=req['o']
        fixedDict['previous_close']=req['pc']
        fixedDict['time_stamp']=req['t']
        fixedDict['difference']=req['c']-req['pc']
        fixedDict['difference_percentage']=100*fixedDict['difference']/req['pc']
        return fixedDict    



    def getRawCandle(self,symbol,resolution='D',count=365):
        requestExtension=('symbol={}&resolution={}&count={}').format(symbol,resolution,count)
        req = requests.get(self.request.format('stock/candle',requestExtension))
        return req.json()


def main():
    a=StockManager()
    #printGraph('AAPL')
    c=a.getRawCandle('AAPL',count=1500)['c']
    print(c)
    print(len(c))

def printGraph(symbol,resolution='D',count=10000):
    a=StockManager()
    c=a.getRawCandle(symbol)['c']
    plt.plot(range(0,len(c)), c)  # Plot some data on the axes.
    plt.show()

if __name__ == "__main__":
    main()

