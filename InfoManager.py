import StockManager
import DatabaseManager

class InfoManager():
    def __init__(self):
        self.stockManager = StockManager.StockManager()
        self.databaseManager = DatabaseManager.DatabaseManager()

    def getStockCandle(self, symbol):
        return self.stockManager.getRawCandle(symbol)

    def getStockQuote(self, symbol):
        return self.stockManager.getQuote(symbol)