import StockManager as SM
import DatabaseManager as DM
import LocalDataManager as LM

timeToResolution={'Y':'D','M':60,'W':30}
resolutionToCount={'D':365,60:720,30:336}
resolutionToTime={'D':'Y',60:'M',30:'W'}
    
def getStockCandle(symbol,timeframe='Y')->dict:
    """get candle from SM
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        resolution {str} -- resolution of checks (default: {'D'})
    
    Returns:
        dict -- candle
    """
    return SM.getCandle(symbol,timeToResolution[timeframe],resolutionToCount[timeToResolution[timeframe]])
    
def getStockQuote(symbol)->dict:
    """get current quote of stock
    
    Arguments:
        symbol {str} -- stock symbol(eg:GOOGL)
    
    Returns:
        dict -- the quote
    """
    return SM.getQuote(symbol)

def getCandle(symbol,timeframe='Y')->dict:
    """general getcandle, decides where to take the candle from
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        timeframe {str} -- the timeframe of the candle (default: {'Y'})
    
    Returns:
        dict -- candle
    """
    #TODO - add database switching
    
    #Get the locally stored data
    localData = LM.getData(symbol, "candle", timeframe)
    #If the data searched for is not in the local storage, put it there from the API
    if localData == {}:
        stockData = getStockCandle(symbol,timeframe)
        #Put the timeframe into the data
        stockData["timeframe"] = timeframe
        LM.putData(symbol, "candle", stockData)
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

#TODO make function threaded
def updateDBFromSM(symbol,timeframe='Y')->dict:
    """get candle from SM and store to DB
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        timeframe {str} -- the timeframe of the candle (default: {'Y'})
    
    Returns:
        dict -- candle
    """
    oCandle=getStockCandle(symbol, timeframe)
    oCandle["timeframe"] = timeframe
    #make threaded
    DM.storeData(symbol, oCandle)
    #copy dictionary
    return oCandle


def main():
    print(getCandle('AAPL'))

if __name__ == "__main__":
    main()