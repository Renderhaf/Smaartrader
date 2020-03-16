from StockManager import StockManager as SM
from DatabaseManager import DatabaseManager as DM

class InfoManager():
    #how does the resolution/count ratio work?
    timeToResolution={'Y':'D','M':60,'W':30}
    resolutionToCount={'D':365,60:720,30:336}
    resolutionToTime={'D':'Y',60:'M',30:'W'}
    
    @staticmethod
    def getStockCandle(symbol,resolution='D',count=365)->dict:
        """get candle from SM
        
        Arguments:
            symbol {str} -- stock symbol(eg:AAPL)
        
        Keyword Arguments:
            resolution {str} -- resolution of checks (default: {'D'})
        
        Returns:
            dict -- candle
        """
        return SM.getCandle(symbol,resolution,count)
    
    @staticmethod
    def getStockQuote(symbol)->dict:
        """get current quote of stock
        
        Arguments:
            symbol {str} -- stock symbol(eg:GOOGL)
        
        Returns:
            dict -- the quote
        """
        return SM.getQuote(symbol)
    

    @staticmethod
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
        if resolution in InfoManager.resolutionToTime.keys():
            #updated DB
            if DM.updated():
                return InfoManager.getDBCandle()
            else:
                #not updated,update and get from stock manger
                return InfoManager.updateDBFromSM(symbol,resolution)
        else:
            #not a regular DB option, get from stock manager
            return InfoManager.getStockCandle(symbol,resolution,InfoManager.resolutionToCount[resolution])

    @staticmethod
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
    
    #
    #TODO make function threaded
    @staticmethod
    def updateDBFromSM(symbol,resolution='D')->dict:
        """get candle from SM and store to DB
        
        Arguments:
            symbol {str} -- stock symbol(eg:AAPL)
        
        Keyword Arguments:
            resolution {str} -- resolution of checks (default: {'D'})
        
        Returns:
            dict -- candle
        """
        oCandle=SM.getCandle(symbol,resolution,InfoManager.resolutionToCount[resolution])
        #make threaded
        DM.storeData(oCandle,symbol,resolution)
        #copy dictionary
        return dict(oCandle)


def main():
    print(InfoManager.getCandle('AAPL'))

if __name__ == "__main__":
    main()