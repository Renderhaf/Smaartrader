import StockManager as SM
import DatabaseManager as DM
import LocalDataManager as LM
import DataValidator as DV
import threading

timeToResolution={'Y':'D','M':'D','W':30}
timeToCount={'Y':365,"M":30,"W":336}
    
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
    #TODO - add database switching
    
    if forceAPI:
        return getStockCandle(symbol, timeframe)

    #Get the locally stored data
    localData = LM.getData(symbol, "candle", timeframe)
    #If the data searched for is not in the local storage, put it there from the API
    if len(localData.keys()) == 0:
        stockData = getStockCandle(symbol,timeframe)
        #Make sure the data from the API is not empty (which could happen in case of an error or an API overload)
        if len(stockData.keys()) == 0:
            #Get Data from the database
            databaseData = getDBCandle(symbol, timeframe)
            return databaseData
        #Put the timeframe into the data
        updateLMfromData(stockData, symbol, timeframe)
        #Update the database
        updateDBFromData(stockData, symbol, timeframe)
        return stockData
    else:
        return localData

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