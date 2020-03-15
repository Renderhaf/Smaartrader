import pymongo


class DatabaseManager():
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://StockManager:Manage123@maincluster-zlnck.mongodb.net/test?retryWrites=true&w=majority")
        self.database = self.client.get_database("StocksInfo")
