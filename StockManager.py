import requests
import json
import time
import matplotlib.pyplot as plt
import numpy as np
import time

file = open("APIKEYS.json", "r")
data = json.loads(file.read())
key = data["Finnhub"]

request = "https://finnhub.io/api/v1/{}?{}&token=" + key
backLoggingAttempts = 5
months={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

maxAPICallsPerMinute = 45
lastCallTimes = []

#delete help variables
file.close()
del data
del key
del file

def getRawQuote( symbol) -> dict:
    """get current quote of stock-uneditted
    
    Arguments:
        symbol {str} -- stock symbol(eg:GOOGL)
    
    Returns:
        dict -- the quote
    """
    req = requests.get(request.format('quote','symbol='+symbol))
    return req.json()

def getQuote(symbol)->dict:
    """get current quote of stock- editted
    
    Arguments:
        symbol {str} -- stock symbol(eg:GOOGL)
    
    Returns:
        dict -- the quote
    """
    req = getRawQuote(symbol)
    fixedDict=dict()
    fixedDict["stockSymbol"]=symbol
    readableSplittedTime=time.ctime(req['t']).split()
    readableTime=readableSplittedTime[2] + '.' + months[readableSplittedTime[1]] + '.' + readableSplittedTime[4]
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

def getRawCandle(symbol,resolution='D',count=365)->dict:
    """get candle of stock-uneditted
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        resolution {str} -- resolution of checks (default: {'D'})
    
    Returns:
        dict -- candle
    """

    #For now, this is here because we need to assign the filtered value of the list to itself
    #TODO - find a way to do this without a global var
    global lastCallTimes

    #Remove old calls from the call list
    currentTime = time.time()
    lastCallTimes = list(filter(lambda callTime : currentTime - callTime < 60 ,lastCallTimes))

    #Dont call the API if we reached the max API calls per minute
    if len(lastCallTimes) >= maxAPICallsPerMinute:
        return dict()

    requestExtension=('symbol={}&resolution={}&count={}').format(symbol,resolution,count)
    req = requests.get(request.format('stock/candle',requestExtension))

    #As soon as we call the API, put the time into the call list
    lastCallTimes.append(time.time())

    #Read the request
    try:
        data = req.json()
    except json.decoder.JSONDecodeError:
        return dict()
    return data

def getCandle(symbol,resolution='D',count=365)->dict:
    """get candle of stock- editted ,added readable date and difference+percentage 
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        resolution {str} -- resolution of checks (default: {'D'})
    
    Returns:
        dict -- candle
    """
    req=getRawCandle(symbol,resolution,count)

    #Make sure data is not empty
    if len(req.keys()) == 0:
        return dict()

    #format the dictionary and add custom values
    #dict_keys(['c' closed, 'h' high, 'l' low, 'o' open, 's' ok or no data, 't timestamp', 'v' volume])
    req['dt']=list()
    req['df']=list()
    req['dfp']=list()
    for i in range(len(req['c'])):
        readableSplittedTime=time.ctime(req['t'][i]).split()
        #dd.mm.yy
        readableDate=readableSplittedTime[2] + '.' + months[readableSplittedTime[1]] + '.' + readableSplittedTime[4]
        if len(str(readableSplittedTime[2]))<2:
            readableDate='0'+readableDate
            
        req['dt'].append(readableDate)
        
        req['df'].append(round(req['c'][i]-req['c'][i-1],2) if i>0 else 0)
        #day's difference percentage
        req['dfp'].append(round(100*req['df'][i]/req['c'][i-1],2) if i>0 else 0)
    return req


def main():
    #printGraph('AAPL','D',30)
    print(getCandle('AAPL','D',30)['dt'] )
    #print(getQuote("AAPL"))

"""print stocks data graph
"""
def printGraph(symbol,resolution='D',count=365):
    can=getCandle(symbol,resolution,count)
    c=can['c']
    plt.plot(range(0,len(c)), c)  # Plot some data on the axes.
    plt.show()

if __name__ == "__main__":
    main()