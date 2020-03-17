import json
import requests
import os
import time
from flask import Flask, render_template, request, flash
import time

import InfoManager as IM

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['HOST'] = 'localhost'


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        # print(request.form["type"], request.form["name"], request.form["time"])
        if request.form["type"] == "quote+candle":
            data = IM.getStockQuote(request.form["name"])
            candleData = IM.getStockCandle(request.form["name"], request.form["time"])
            data["prices"] = candleData["c"]
            data["dates"] = [time.ctime(t) for t in candleData["t"]]
            return data

        if request.form["type"] == "candle":
            stockData = IM.getStockCandle(request.form["name"], request.form["time"])
            prices = stockData["c"]
            dates = [time.ctime(t) for t in stockData["t"]]
            data = {"prices":prices, "dates":dates}
            return data

        if request.form["type"] == "quote":
            return IM.getStockQuote(request.form["name"])


    else: 
        return render_template("index.html", stocks = ["AAPL", "GOOGL", "TEVA"])

if __name__ == "__main__":
    port = os.environ.get('PORT') or 5000
    app.run(host='0.0.0.0', port=int(port))