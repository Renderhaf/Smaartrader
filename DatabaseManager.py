import pymongo


client = pymongo.MongoClient("mongodb+srv://StockManager:Manage123@maincluster-zlnck.mongodb.net/test?retryWrites=true&w=majority")
database =client.get_database("StocksInfo")
#TODO find out resolutions meaning

isUpdated=False


def updated():
    return False
    #TODO write real updated checker

def storeData(candle,symbol,resolution):
    pass

def getData(symbol,resolution):
    pass
