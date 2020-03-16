import pymongo


class DatabaseManager():
    client = pymongo.MongoClient("mongodb+srv://StockManager:Manage123@maincluster-zlnck.mongodb.net/test?retryWrites=true&w=majority")
    database =client.get_database("StocksInfo")
    #ToDo find out resolutions meaning
    
    isUpdated=False

    @staticmethod
    def updated():
        return False
        #ToDo write real updated checker
    
    @staticmethod
    def storeData(candle,symbol,resolution):
        pass

    @staticmethod
    def getData(symbol,resolution):
        pass
    