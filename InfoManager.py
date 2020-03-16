import StockManager as SM
import DatabaseManager as DM


class InfoManager():
    #how does the resolution/count ratio work?
    timeToResolution={'Y':'D','M':60,'W':30}
    resolutionToCount={'D':365,60:720,30:336}
    resolutionToTime={'D':'Y',60:'M',30:'W'}
    
    @staticmethod
    def getStockCandle(symbol,resolution='D',count=365)->dict:
        return SM.StockManager.getCandle(symbol,resolution,count)
    
    @staticmethod
    def getStockQuote(symbol)->dict:
        return SM.StockManager.getQuote(symbol)
    
    @staticmethod
    def getCandle(symbol,resolution='D')->dict:
        #one of the options in DB
        if resolution in InfoManager.resolutionToTime.keys():
            if DM.DatabaseManager.updated()==True:
                return InfoManager.getDBCandle()
            else:
                return InfoManager.updateDBFromSM(symbol,resolution)
        else:
            return InfoManager.getStockCandle(symbol,resolution,InfoManager.resolutionToCount[resolution])


    @staticmethod
    def getDBCandle(symbol,resolution='D')->dict:
        oCandle = DM.DatabaseManager.getData(symbol,resolution)
        return dict(oCandle)
    
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