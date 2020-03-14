import pymongo

client = pymongo.MongoClient("mongodb+srv://StockManager:Manage123@maincluster-zlnck.mongodb.net/test?retryWrites=true&w=majority")
quary = client["StocksInfo"]["AAPL"]
print(quary.)