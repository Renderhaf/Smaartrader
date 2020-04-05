import json
import os
import sys
import time

import requests
from flask import Flask, make_response, render_template, request, jsonify

#This is a module for Web Security, its currently used for sessions and CSRF protection
import WebSecurity
WebSecurity.resetStorage()

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
    if request.method == "POST": #POST
        if not WebSecurity.validatePOST(request):
            return "Bad request. The server could not validate this POST request", 403 #Forbidden Request Status Code
        
        try: #These are put in a try except block in order to prevent crashing when bad post requests are sent
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

        except Exception as err:
            print("Internal Server Error: ", err)
            return "Internal Server Error", 500 #Internal Server Error Status Code
            
        except KeyError:
            pass

        return "Bad request. The request is missing required keys", 400 #Bad Request Status Code

        
    else: #GET
        viewedStocks = companies
        response = ""
        if len(viewedStocks) > 10:
            response =  render_template("oneRequestIndex.html", stocks = viewedStocks)
        else:
            response =  render_template("threadedRequestIndex.html", stocks = viewedStocks)

        response = make_response(response)

        #Decide whether this request needs a new sessionID
        currentSessionID = request.cookies.get('sessionID', default="")
        if not WebSecurity.isSessionStored(currentSessionID):
            response.set_cookie("sessionID", WebSecurity.getNewSessionID())
        return response

if __name__ == "__main__":
    port = os.environ.get('PORT') or 5000
    app.run(host='0.0.0.0', port=int(port))