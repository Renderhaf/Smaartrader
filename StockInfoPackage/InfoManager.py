import FinnhubStockManager as SM
import FinModelStockManager as NSM
import DatabaseManager as DM
import LocalDataManager as LM
import DataValidator as DV
import threading
import json
import os 

regressionLimit = 3

DEBUG = True

default_quality='high'

#Get the list of avilable stocks\cryptos and their names
with open(os.path.abspath("./Datafiles/stockTickers.json"), "r") as stockFile, open(os.path.abspath("./Datafiles/cryptoTickers.json"), "r") as cryptoFile:
    tickerData:dict = json.loads(stockFile.read())
    cryptoTickers:dict = json.loads(cryptoFile.read())


def getName(ticker:str)->str:
    '''
    Gets the name of the stock based on its ticket. If the ticker does not have a name, the ticker is returned back
    '''
    stockName = tickerData.get(ticker, ticker)
    if stockName == ticker:
        return cryptoTickers.get(ticker, ticker)  
    return stockName

def isAnExistingTicker(ticker:str)->bool:
    '''
    Checks if the ticker is the the pool of tickers
    '''
    return ticker in tickerData.keys() or ticker in cryptoTickers.keys()

'''
Helper Functions
'''
def removeKey(data:dict, key:str)->None:
    try:
        data.pop(key)
    except Exception:
        return

'''
States and state order for candle supplier
'''
def candleStockAPIState(symbol, timeframe, quality):
    if DEBUG:
        print("{} : Entered stock candle state".format(symbol))
    stockData = getStockCandle(symbol,timeframe,quality)  

    #This is here so that when given empty data, the quary will go back upto regressionLimit (currently 3) days
    for i in range(regressionLimit):
        #No data in the candle
        if len(stockData.keys()) == 0 or stockData["s"] == "no_data":
            #Check again
            stockData = getStockCandle(symbol, timeframe,quality, timeMul=i+1)
        else:
            break
    #The for looped for regressionLimit times, and did not find anything
    else:
        print("Shit. This wasn't supposed to happen")
        return dict()

    #make sure that the data is not empty
    if len(stockData.keys()) == 0:
        return dict()
    #Update the local storage
    updateLMfromData(stockData, symbol, timeframe,quality)
    #Update the database
    updateDBFromData(stockData, symbol, timeframe,quality)
    
    return stockData

def candleLocalStorageState(symbol, timeframe, quality=default_quality):
    if DEBUG:
        print("{} : Entered local candle state".format(symbol))
    return LM.getData(symbol, timeframe, quality)

def candleDatabaseState(symbol, timeframe,quality=default_quality):
    if DEBUG:
        print("{} : Entered database candle state".format(symbol))

    data = getDBData(symbol, timeframe, quality)
    return data

candleStateOrder = [candleLocalStorageState, candleStockAPIState, candleDatabaseState]


'''
States and state oreder for quote supplier
'''
def quoteStockState(symbol):
    if DEBUG:
        print("{} : Entered stock quote state".format(symbol))
        
    quote = getStockQuote(symbol)

    if len(quote.keys()) == 0:
        return dict()
    #Update the local storage
    updateLMfromData(quote, symbol, "Q", "high")
    #Update the database
    updateDBFromData(quote, symbol, "Q", "high")

    return quote

def quoteLocalState(symbol):
    if DEBUG:
        print("{} : Entered local quote state".format(symbol))
    return LM.getData(symbol, "Q", "high")


def quoteDatabaseState(symbol):
    if DEBUG:
        print("{} : Entered database quote state".format(symbol))
    data = getDBData(symbol, "Q", "high")
    return data

quoteStateOrder = [quoteLocalState, quoteStockState, quoteDatabaseState]

'''
Suppliers
'''    
def getStockCandle(symbol,timeframe='Y', quality=default_quality, timeMul=0)->dict:
    """get candle from SM
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        timeframe {str} -- the timeframe of the candle (default: {'Y'})
        timeMul {int} -- the amount of counts to be added
    
    Returns:
        dict -- candle
    """
    qualities={'high':{'TTR':{'Y':'D','M':'D','W':30,'D':5},'TTC':{'Y':365,'M':30,'W':336,'D':288}},
           'low':{'TTR':{'Y':'W','M':'D','W':60,'D':30},'TTC':{'Y':52,'M':30,'W':168,'D':48}}}
    isCrypto = symbol in cryptoTickers.keys()

    if timeframe == 'A':
        if quality in qualities.keys():
            data = NSM.getAllHistoricData(symbol, quality, isCrypto=isCrypto)
        else:
            data = NSM.getAllHistoricData(symbol, default_quality, isCrypto=isCrypto)
        return data

    timeToResolution={'Y':'D','M':'D','W':30,'D':5}

    if isCrypto:
        if quality in qualities.keys():
            data = NSM.getCandle(symbol, timeframe, quality, isCrypto=True)

        else:
            if DEBUG:
                print('Not a quality')
            data = NSM.getCandle(symbol, "Y", "high")
    else:
        if quality in qualities.keys():
            data = SM.getCandle(symbol,qualities[quality]['TTR'][timeframe],(1 + timeMul)*qualities[quality]['TTC'][timeframe])

        else:
            if DEBUG:
                print('Not a quality')
            data = SM.getCandle(symbol,qualities[default_quality]['TTR'][timeframe],(1 + timeMul)*qualities[default_quality]['TTC'][timeframe])
    
    return data

def getStockQuote(symbol)->dict:
    """get current quote of stock
    
    Arguments:
        symbol {str} -- stock symbol(eg:GOOGL)
    
    Returns:
        dict -- the quote
    """
    if symbol in cryptoTickers.keys():
        return NSM.getQuote(symbol)
    else:
        return SM.getQuote(symbol)

def getCandle(symbol,timeframe='Y', quality=default_quality, forceAPI=False)->dict:
    """general getcandle, decides where to take the candle from
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        timeframe {str} -- the timeframe of the candle (default: {'Y'})
    
    Returns:
        dict -- candle
    """    

    if forceAPI:
        return getStockCandle(symbol, timeframe,quality)


    for state in candleStateOrder:
        data = state(symbol, timeframe,quality)
        if len(data.keys()) != 0:
            return data

def getQuote(symbol:str, forceAPI:bool=False)->dict:
    """general getQuote, decides where to take the quote from
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Returns:
        dict -- quote
    """  
    if forceAPI:
        return getStockQuote(symbol)


    for state in quoteStateOrder:
        data = state(symbol)
        if len(data.keys()) != 0:
            return data


def getDBData(symbol,timeframe='Y', quality=default_quality)->dict:
    """get candle from DB
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        timeframe {str} -- the timeframe of the candle (default: {'Y'})
    
    Returns:
        dict -- candle
    """
    return DM.getData(symbol,timeframe,quality)

def updateLMfromData(data, symbol, timeframe='Y', quality=default_quality)->None:
    """this function updated the local storage from data given
    
    Arguments:
        data {dict} -- the data to be stored
        symbol {str} -- stock symbol
    
    Keyword Arguments:
        timeframe {str} -- the timeframe of the candle (default: {'Y'})
    """
    data["timeframe"] = timeframe
    data["quality"] = quality
    LM.putData(symbol, data)

def updateDBFromData(data, symbol,timeframe='Y', quality=default_quality)->None:
    """get candle from SM and store to DB
    
    Arguments:
        data {dict} -- the data to be uploaded
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        timeframe {str} -- the timeframe of the candle (default: {'Y'})
    
    Returns:
        None
    """
    data["timeframe"] = timeframe
    data["quality"] = quality
    DV.putExpirationDate(data)
    #start a new thread for uploading the info to the database
    threading.Thread(target=DM.storeData, args=[symbol,data]).start()


def main():
    STOCKNAME = "BTCUSD"

    # print(len(getCandle(STOCKNAME, 'D', quality="low")['c']))
    # print(getCandle(STOCKNAME, timeframe="Y"))

if __name__ == "__main__":
    main()
