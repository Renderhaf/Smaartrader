import json
import requests
import os
import time
from flask import Flask, render_template, request
import json
import time
import sys

#This adds the StockInfoPackage package to the path, so we can import from it
sys.path.insert(1, './StockInfoPackage/')

import InfoManager as IM

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['HOST'] = 'localhost'

with open("companies.json", "r") as file:
    companies = json.loads(file.read())

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["type"] == "quote+candle":
            if request.form["isMulti"] == 'true':
                symbolData = {}
                for symbol in json.loads(request.form["names"]):
                    data = IM.getStockQuote(symbol)
                    candleData = IM.getCandle(symbol, request.form["time"])
                    data["prices"] = candleData["c"]
                    data["dates"] = [time.ctime(t) for t in candleData["t"]]
                    symbolData[symbol] = data
                return symbolData
            else:
                data = IM.getStockQuote(request.form["name"])
                candleData = IM.getCandle(request.form["name"], request.form["time"])
                data["prices"] = candleData["c"]
                data["dates"] = [time.ctime(t) for t in candleData["t"]]
                return data

        if request.form["type"] == "candle":
            stockData = IM.getCandle(request.form["name"], request.form["time"])
            prices = stockData["c"]
            dates = [time.ctime(t) for t in stockData["t"]]
            data = {"prices":prices, "dates":dates}
            return data

        if request.form["type"] == "quote":
            return IM.getStockQuote(request.form["name"])


    else: 
        viewedStocks = companies
        if False:
            return render_template("oneRequestIndex.html", stocks = viewedStocks)
        else:
            return render_template("threadedRequestIndex.html", stocks = viewedStocks)

if __name__ == "__main__":
    port = os.environ.get('PORT') or 5000
    app.run(host='0.0.0.0', port=int(port))