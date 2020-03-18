import StockManager as SM
import DatabaseManager as DM
import LocalDataManager as LM
import DataValidator as DV
import threading

timeToResolution={'Y':'D','M':'D','W':30}
timeToCount={'Y':365,"M":30,"W":336}

DEBUG = True

def candleStockAPIState(symbol, timeframe):
    if DEBUG:
        print("{} : Entered stock state".format(symbol))
    stockData = getStockCandle(symbol,timeframe)
    #make sure that the data is not empty
    if len(stockData.keys()) == 0:
        return dict()
    #Update the local storage
    updateLMfromData(stockData, symbol, timeframe)
    #Update the database
    updateDBFromData(stockData, symbol, timeframe)
    return stockData

def candleLocalStorageState(symbol, timeframe):
    if DEBUG:
        print("{} : Entered local state".format(symbol))
    return LM.getData(symbol, "candle", timeframe)

def candleDatabaseState(symbol, timeframe):
    if DEBUG:
        print("{} : Entered database state".format(symbol))
    return getDBCandle(symbol, timeframe)

candleStateOrder = [candleLocalStorageState, candleStockAPIState, candleDatabaseState]

    
def getStockCandle(symbol,timeframe='Y')->dict:
    """get candle from SM
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        resolution {str} -- resolution of checks (default: {'D'})
    
    Returns:
        dict -- candle
    """
    return SM.getCandle(symbol,timeToResolution[timeframe],timeToCount[timeframe])
    
def getStockQuote(symbol)->dict:
    """get current quote of stock
    
    Arguments:
        symbol {str} -- stock symbol(eg:GOOGL)
    
    Returns:
        dict -- the quote
    """
    return SM.getQuote(symbol)

def getCandle(symbol,timeframe='Y', forceAPI=False)->dict:
    """general getcandle, decides where to take the candle from
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        timeframe {str} -- the timeframe of the candle (default: {'Y'})
    
    Returns:
        dict -- candle
    """    
    if forceAPI:
        return getStockCandle(symbol, timeframe)


    for state in candleStateOrder:
        data = state(symbol, timeframe)
        if len(data.keys()) != 0:
            return data


def getDBCandle(symbol,timeframe='Y')->dict:
    """get candle from DB
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        timeframe {str} -- the timeframe of the candle (default: {'Y'})
    
    Returns:
        dict -- candle
    """
    return DM.getData(symbol,timeframe)

def updateLMfromData(data, symbol, timeframe='Y')->None:
    """this function updated the local storage from data given
    
    Arguments:
        data {dict} -- the data to be stored
        symbol {str} -- stock symbol
    
    Keyword Arguments:
        timeframe {str} -- the timeframe of the candle (default: {'Y'})
    """
    data["timeframe"] = timeframe
    LM.putData(symbol, "candle", data)

def updateDBFromData(data, symbol,timeframe='Y')->None:
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
    DV.putExpirationDate(data)
    #start a new thread for uploading the info to the database
    threading.Thread(target=DM.storeData, args=[symbol,data]).start()

def main():
    print(getCandle('AAPL'))

if __name__ == "__main__":
    main()