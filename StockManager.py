import requests
import json
import time
import matplotlib.pyplot as plt
import numpy as np

"""
class to handle all stocks get information
"""
class StockManager():
    
    
    def __init__(self):
        self.months={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        with open("APIKEYS.json", "r") as file:
            data = json.loads(file.read())
            key = data["Finnhub"]
        self.request = "https://finnhub.io/api/v1/{}?{}&token=" + key
        self.backLoggingAttempts = 5
    
    """
    get stock quote
    
    Returns:
        [dict] -- [get raw quote from api]
    """
    def getRawQuote(self, symbol) -> dict:
        req = requests.get(self.request.format('quote','symbol='+symbol))
        return req.json()

    """
    modify quote to be more accesible
    
    Returns:
        [dict] -- [the modified quote]
    """
    def getQuote(self,symbol)->dict:
        req = self.getRawQuote(symbol)
        fixedDict=dict()
        fixedDict["stockSymbol"]=symbol
        readableSplittedTime=time.ctime(req['t']).split()
        readableTime=readableSplittedTime[2] + '.' + self.months[readableSplittedTime[1]] + '.' + readableSplittedTime[4]
        fixedDict['date']=readableTime
        fixedDict['current_price']= round(req['c'],2)
        fixedDict['today_high']=req['h']
        fixedDict['today_low']=req['l']
        fixedDict['open_price']=req['o']
        fixedDict['previous_close']=req['pc']
        fixedDict['time_stamp']=req['t']
        fixedDict['difference']= round(req['c']-req['pc'],2)
        fixedDict['difference_percentage']= round(100*fixedDict['difference']/req['pc'],2)
        return fixedDict


    """raw candle data
    stocks over time
    Returns:
        [dict] -- [dictionary of stocks data over time]
    """
    def getRawCandle(self,symbol,resolution='D',count=365)->dict:
        # #If you are on a weekend, the 
        # if time.asctime().split(" ")[0] in ["Sat", "Sun"]:

        requestExtension=('symbol={}&resolution={}&count={}').format(symbol,resolution,count)
        req = requests.get(self.request.format('stock/candle',requestExtension))
        data = req.json()
        return data

    """candle data
    modified stocks over time
    Returns:
        [dict] -- [dictionary of stocks data over time, sorted by time]
    """
    def getCandle(self,symbol,resolution='D',count=365)->dict:
        req=self.getRawCandle(symbol,resolution,count)
        fixedList=dict()
        #dict_keys(['c' closed, 'h' high, 'l' low, 'o' open, 's' ok or no data, 't timestamp', 'v' volume])
        for i in range(len(req['c'])):
            s=dict()
            readableSplittedTime=time.ctime(req['t'][i]).split()
            #dd.mm.yy
            readableTime=readableSplittedTime[2] + '.' + self.months[readableSplittedTime[1]] + '.' + readableSplittedTime[4]
            #date
            #s['dt']=readableTime
            #closed price
            s['c']=req['c'][i]
            #timestamp
            s['t']=req['t'][i]
            #open price
            s['o']=req['o'][i]
            #volume-number of buys
            s['v']=req['v'][i]
            #day's high price
            s['h']=req['h'][i]
            #day's low price
            s['l']=req['l'][i]
            #day's difference
            s['df']= round(req['c'][i]-req['c'][i-1],2) if i>0 else 0
            #day's difference percentage
            s['dfp']= round(100*s['df']/req['c'][i-1],2) if i>0 else 0
            fixedList[readableTime]=s
        return fixedList

def main():
    a=StockManager()
    #printGraph('GOOGL')

"""print stocks data graph
"""
def printGraph(symbol,resolution='D',count=365):
    a=StockManager()
    can=a.getCandle(symbol,resolution,count)
    c=[s['c'] for s in can.values()]
    plt.plot(range(0,len(c)), c)  # Plot some data on the axes.
    plt.show()

if __name__ == "__main__":
    main()