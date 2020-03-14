import requests
import json

class StockManager():
    def __init__(self):
        with open("APIKEYS.json", "r") as file:
            data = json.loads(file.read())
            key = data["Finnhub"]
        self.request = "https://finnhub.io/api/v1/quote?symbol={}&token=" + key
    
    def getRawQuote(self, symbol) -> dict:
        req = requests.get(self.request.format(symbol))
        return req.json()
    
    def getQuote(self,symbol):
        req = self.getRawQuote(symbol)
        fixedDict=dict()
        fixedDict['current_price']=req['c']
        fixedDict['today_high']=req['h']
        fixedDict['today_low']=req['l']
        fixedDict['open_price']=req['o']
        fixedDict['previous_close']=req['pc']
        fixedDict['time_stamp']=req['t']
        fixedDict['difference']=req['c']-req['pc']
        fixedDict['difference_percentage']=100*fixedDict['difference']/req['pc']
        return fixedDict
        
a=StockManager()      
print(a.getQuote('AAPL'))
