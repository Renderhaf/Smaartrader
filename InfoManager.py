import StockManager
import DatabaseManager

class InfoManager():
    def __init__(self):
        self.stockManager = StockManager.StockManager()
        self.databaseManager = DatabaseManager.DatabaseManager()

    def getStockCandle(self, symbol, time="Y"):
        if time=="Y":
            return self.stockManager.getRawCandle(symbol)
        elif time=="M":
            return self.stockManager.getRawCandle(symbol, count=720, resolution=60)
        elif time=="W":
            return self.stockManager.getRawCandle(symbol, count=336, resolution=30)

    def getStockQuote(self, symbol):
        return self.stockManager.getQuote(symbol)