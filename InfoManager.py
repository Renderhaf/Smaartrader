import StockManager as SM
import DatabaseManager as DM


class InfoManager():
    #how does the resolution/count ratio work?
    timeToResolution={'Y':'D','M':60,'W':30}
    resolutionToCount={'D':365,60:720,30:336}
    resolutionToTime={'D':'Y',60:'M',30:'W'}
    
    """get stock candle data form stock manager
    
    Returns:
        [dict] -- [candle]
    """
    @staticmethod
    def getStockCandle(symbol,resolution='D',count=365)->dict:
        return SM.StockManager.getCandle(symbol,resolution,count)
    
    """get stocks current quote from stock manager
    
    Returns:
        [dict] -- [cuurent quote data]
    """
    @staticmethod
    def getStockQuote(symbol)->dict:
        return SM.StockManager.getQuote(symbol)
    
    """general get candle, checks where to get it from
    
    Returns:
        [dict] -- [candle stock data]
    """
    @staticmethod
    def getCandle(symbol,resolution='D')->dict:
        #one of the options in DB
        if resolution in InfoManager.resolutionToTime.keys():
            #updated DB
            if DM.DatabaseManager.updated():
                return InfoManager.getDBCandle()
            else:
                #not updated,update and get from stock manger
                return InfoManager.updateDBFromSM(symbol,resolution)
        else:
            #not a regular DB option, get from stock manager
            return InfoManager.getStockCandle(symbol,resolution,InfoManager.resolutionToCount[resolution])

    """get candle from Database
    
    Returns:
        [dict] -- [candle of stock]
    """
    @staticmethod
    def getDBCandle(symbol,resolution='D')->dict:
        oCandle = DM.DatabaseManager.getData(symbol,resolution)
        return dict(oCandle)
    
    """update database and get data from stock manager
    
    Returns:
        [dict] -- [candle]
    """
    #ToDo make function threded
    @staticmethod
    def updateDBFromSM(symbol,resolution='D')->dict:
        oCandle=SM.StockManager.getCandle(symbol,resolution,InfoManager.resolutionToCount[resolution])
        #make threaded
        DM.DatabaseManager.storeData(oCandle,symbol,resolution)
        #copy dictionary
        return dict(oCandle)


def main():
    print(InfoManager.getCandle('AAPL'))

if __name__ == "__main__":
    main()