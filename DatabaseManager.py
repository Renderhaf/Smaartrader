import pymongo


class DatabaseManager():
    client = pymongo.MongoClient("mongodb+srv://StockManager:Manage123@maincluster-zlnck.mongodb.net/test?retryWrites=true&w=majority")
    database =client.get_database("StocksInfo")
    isUpdated=False

    @staticmethod
    def updated():
        return False
        #ToDo write real updated checker
    
    @staticmethod
    def storeData(symbol,resolution):
        raise NotImplementedError

    @staticmethod
    def getData(symbol,resolution):
        raise NotImplementedError
    