import pymongo
import DataValidator as DV

client = pymongo.MongoClient("mongodb+srv://StockManager:Manage123@maincluster-zlnck.mongodb.net/test?retryWrites=true&w=majority")
database = client.get_database("StocksInfo")

def storeData(symbol, data):
    timeframe = data["timeframe"]
    currentStoredData = getData(symbol, timeframe)
    #If the data is expired, remove it
    if DV.isExpired(currentStoredData):
        removeData(symbol, timeframe)
        currentStoredData = {}
    #If the data is not already there store it
    if currentStoredData == {}:
        #Store the data
        collection = database.get_collection(symbol)
        newdata = data
        DV.putExpirationDate(newdata)
        collection.insert_one(newdata)

def removeData(symbol, timeframe):
    collection = database.get_collection(symbol)
    collection.delete_one({"timeframe": timeframe})

def getData(symbol, timeframe):
    collection = database.get_collection(symbol)
    data = list(collection.find({"timeframe": timeframe}))
    if len(data) == 0:
        return {}
    else:
        return data[0]

def test():
    # storeData("GOOGL", {"prices": [1,2,3,4], "timeframe": "Y"})
    # removeData("GOOGL", "Y")
    print(getData("GOOGL", "Y"))

if __name__ == "__main__":
    test()