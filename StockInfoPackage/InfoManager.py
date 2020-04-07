import StockManager as SM
import DatabaseManager as DM
import LocalDataManager as LM
import DataValidator as DV
import threading

qualities={'high':{'TTR':{'Y':'D','M':'D','W':30,'D':5},'TTC':{'Y':365,'M':30,'W':336,'D':288}},\
    'low':{'TTR':{'Y':'W','M':'D','W':60,'D':30},'TTC':{'Y':52,'M':30,'W':168,'D':48}}}

timeToResolution={'Y':'D','M':'D','W':30,'D':5}
timeToCount={'Y':365,'M':30,'W':336,'D':288}
regressionLimit = 3

DEBUG = True

default_quality='high'

def candleStockAPIState(symbol, timeframe, quality):
    if DEBUG:
        print("{} : Entered stock state".format(symbol))
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
        print("{} : Entered local state".format(symbol))
    return LM.getData(symbol, "candle", timeframe,quality)

def candleDatabaseState(symbol, timeframe,quality=default_quality):
    if DEBUG:
        print("{} : Entered database state".format(symbol))
    return getDBCandle(symbol, timeframe,quality)

candleStateOrder = [candleLocalStorageState, candleStockAPIState, candleDatabaseState]
    
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
    if quality in qualities.keys():
        return SM.getCandle(symbol,qualities[quality]['TTR'][timeframe],(1 + timeMul)*qualities[quality]['TTC'][timeframe])
    else:
        if DEBUG:
            print('Not a quality')
        return SM.getCandle(symbol,qualities[default_quality]['TTR'][timeframe],(1 + timeMul)*qualities[default_quality]['TTC'][timeframe])

def getStockQuote(symbol)->dict:
    """get current quote of stock
    
    Arguments:
        symbol {str} -- stock symbol(eg:GOOGL)
    
    Returns:
        dict -- the quote
    """
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


def getDBCandle(symbol,timeframe='Y', quality=default_quality)->dict:
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
    LM.putData(symbol, "candle", data)

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
    print(len(getCandle('AAPL', 'D')['c']))

if __name__ == "__main__":
    main()
