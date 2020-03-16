import requests
import json
import time
import matplotlib.pyplot as plt
import numpy as np

"""
class to handle all stocks get information
"""
class StockManager():
    #static 
    with open("APIKEYS.json", "r") as file:
        data = json.loads(file.read())
        key = data["Finnhub"]
    request = "https://finnhub.io/api/v1/{}?{}&token=" + key
    backLoggingAttempts = 5
    months={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

    @staticmethod
    def getRawQuote( symbol) -> dict:
        """
        get stock quote
        
        Returns:
            [dict] -- [get raw quote from api]
        """
        req = requests.get(request.format('quote','symbol='+symbol))
        return req.json()

    
    @staticmethod
    def getQuote(symbol)->dict:
        """
        modify quote to be more accesible
        
        Returns:
            [dict] -- [the modified quote]
        """
        req = getRawQuote(symbol)
        fixedDict=dict()
        fixedDict["stockSymbol"]=symbol
        readableSplittedTime=time.ctime(req['t']).split()
        readableTime=readableSplittedTime[2] + '.' + StockManager.months[readableSplittedTime[1]] + '.' + readableSplittedTime[4]
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


    @staticmethod
    def getRawCandle(symbol,resolution='D',count=365)->dict:
        """raw candle data
        stocks over time
        Returns:
            [dict] -- [dictionary of stocks data over time]
        """
        requestExtension=('symbol={}&resolution={}&count={}').format(symbol,resolution,count)
        req = requests.get(StockManager.request.format('stock/candle',requestExtension))
        data = req.json()
        return data


    @staticmethod
    def getCandle(symbol,resolution='D',count=365)->dict:
        """
        candle data - modified stocks over time
        Returns:
            [dict] -- [dictionary of stocks data over time, sorted by time]
        """
        req=StockManager.getRawCandle(symbol,resolution,count)
        #dict_keys(['c' closed, 'h' high, 'l' low, 'o' open, 's' ok or no data, 't timestamp', 'v' volume])
        req['dt']=list()
        req['df']=list()
        req['dfp']=list()
        for i in range(len(req['c'])):
            readableSplittedTime=time.ctime(req['t'][i]).split()
            #dd.mm.yy
            readableDate=readableSplittedTime[2] + '.' + StockManager.months[readableSplittedTime[1]] + '.' + readableSplittedTime[4]
            
            req['dt']=readableDate
            
            req['df'].append(round(req['c'][i]-req['c'][i-1],2) if i>0 else 0)
            #day's difference percentage
            req['dfp'].append(round(100*req['df'][i]/req['c'][i-1],2) if i>0 else 0)
        return req

def main():
    a=StockManager()
    printGraph('GOOGL')

"""print stocks data graph
"""
def printGraph(symbol,resolution='D',count=365):
    a=StockManager()
    can=a.getCandle(symbol,resolution,count)
    c=can['c']
    plt.plot(range(0,len(c)), c)  # Plot some data on the axes.
    plt.show()

if __name__ == "__main__":
    main()