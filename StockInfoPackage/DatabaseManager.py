import pymongo
import DataValidator as DV

client = pymongo.MongoClient("mongodb+srv://StockManager:Manage123@maincluster-zlnck.mongodb.net/test?retryWrites=true&w=majority")
database = client.get_database("StocksInfo")

def storeData(symbol:str, data:dict, quality='high')->None:
    """This function stores candle data in the database, if that same data isn't already stored
    
    Arguments:
        symbol {str} -- [The stock symbol for the data]
        data {dict} -- [the data to be stored]
    """
    timeframe = data["timeframe"]
    currentStoredData = getData(symbol, timeframe, quality)
    #If the data is expired, remove it
    if DV.isExpired(currentStoredData):
        removeData(symbol, timeframe,quality)
        currentStoredData = {}
    #If the data is not already there store it
    if currentStoredData == {}:
        #Store the data
        collection = database.get_collection(symbol)
        newdata = data
        #Put a longer expiration date on the data since its mostly for backup
        DV.putExpirationDate(newdata, 2)
        collection.insert_one(newdata)

def removeData(symbol:str, timeframe:str, quality:str='high')->None:
    """This function removes data from the database
    
    Arguments:
        symbol {str} -- [the stock symbol for the data to be removed (defines the collection the data is in)]
        timeframe {str} -- [the timeframe for the data to be removed]
    """
    collection = database.get_collection(symbol)
    collection.delete_one({"timeframe": timeframe, "quality":quality})

def getData(symbol:str, timeframe:str,quality:str='high')->dict:
    """This function returns candle data from the database
    
    Arguments:
        symbol {str} -- [The stock symbol for the requested data]
        timeframe {str} -- [The timeframe for the requested data]
    
    Returns:
        dict -- [The data requested (if the data does not exist in the database, this will return {})]
    """
    collection = database.get_collection(symbol)
    data = list(collection.find({"timeframe": timeframe,"quality":quality}))
    if len(data) == 0:
        return {}
    else:
        return data[0]

def test():
    # storeData("GOOGL", {"prices": [1,2,3,4], "timeframe": "Y"})
    # removeData("GOOGL", "Y")
    print(getData("TSLA", "Y"))

if __name__ == "__main__":
    test()