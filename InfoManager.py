import StockManager as SM
import DatabaseManager as DM

timeToResolution={'Y':'D','M':60,'W':30}
resolutionToCount={'D':365,60:720,30:336}
resolutionToTime={'D':'Y',60:'M',30:'W'}
    
def getStockCandle(symbol,time='Y')->dict:
    """get candle from SM
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        resolution {str} -- resolution of checks (default: {'D'})
    
    Returns:
        dict -- candle
    """
    return SM.getCandle(symbol,timeToResolution[time],resolutionToCount[timeToResolution[time]])
    
def getStockQuote(symbol)->dict:
    """get current quote of stock
    
    Arguments:
        symbol {str} -- stock symbol(eg:GOOGL)
    
    Returns:
        dict -- the quote
    """
    return SM.getQuote(symbol)

def getCandle(symbol,resolution='D')->dict:
    """general getcandle, decides where to take the candle from
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        resolution {str} -- resolution of checks (default: {'D'})
    
    Returns:
        dict -- candle
    """
    #one of the options in DB
    if resolution in resolutionToTime.keys():
        #updated DB
        if DM.updated():
            return getDBCandle()
        else:
            #not updated,update and get from stock manger
            return updateDBFromSM(symbol,resolution)
    else:
        #not a regular DB option, get from stock manager
        return getStockCandle(symbol,resolution,resolutionToCount[resolution])

def getDBCandle(symbol,resolution='D')->dict:
    """get candle from DB
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        resolution {str} -- resolution of checks (default: {'D'})
    
    Returns:
        dict -- candle
    """
    oCandle = DM.getData(symbol,resolution)
    return dict(oCandle)

#TODO make function threaded
def updateDBFromSM(symbol,resolution='D')->dict:
    """get candle from SM and store to DB
    
    Arguments:
        symbol {str} -- stock symbol(eg:AAPL)
    
    Keyword Arguments:
        resolution {str} -- resolution of checks (default: {'D'})
    
    Returns:
        dict -- candle
    """
    oCandle=SM.getCandle(symbol,resolution,resolutionToCount[resolution])
    #make threaded
    DM.storeData(oCandle,symbol,resolution)
    #copy dictionary
    return dict(oCandle)


def main():
    print(getCandle('AAPL'))

if __name__ == "__main__":
    main()