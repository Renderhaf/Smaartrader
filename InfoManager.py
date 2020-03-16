import StockManager as SM
import DatabaseManager as DM


class InfoManager():
    #how does the resolution/count ratio work?
    timeToResolution=resolutions={'Y':('D',365),'M':(60,720),'W':(30,336)}
    
    @staticmethod
    def getStockCandle(symbol,resolution='D',count=365)->dict:
        return SM.StockManager.getCandle(symbol,resolution,count)
    
    @staticmethod
    def getStockQuote(symbol)->dict:
        return SM.StockManager.getQuote(symbol)
    
    @staticmethod
    def getCandle(symbol,resolution='D',count=-1)->dict:
        #default count as in db
        if count==-1:
            count=DM.DatabaseManager.resolutions[resolution]

        #one of the options in DB
        if resolution in DM.resolutions.keys() and count<=DM.DatabaseManager.resolutions[resolution]:
            if DM.DatabaseManager.updated()==True:
                return InfoManager.getDBCandle()
            else:
                return InfoManager.updateDBFromSM()
        #should't be in DB
        else:
            return InfoManager.getStockCandle(symbol,resolution,count)


    @staticmethod
    def getDBCandle(symbol,resolution='D',count=365)->dict:
        oCandle = DM.DatabaseManager.getData(symbol,resolution)
        return cutDict(oCandle,count)
    
    #ToDo make function threded
    @staticmethod
    def updateDBFromSM(symbol,resolution='D',count=365)->dict:
        oCandle=SM.StockManager.getCandle()
        #make threaded
        DM.DatabaseManager.storeData(oCandle,symbol,resolution)
        #copy dictionary
        return cutDict(oCandle,count)



#copy so its a new dict
def cutDict(oD,count)->dict:
    d=dict()
    for key in oD.keys():
        d[key]=oD[key][0:count]
    return d
    