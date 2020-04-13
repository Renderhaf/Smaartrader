from server import app
from flask import request, render_template, redirect, make_response
import time
import sys 
import json

import WebSecurity
WebSecurity.resetStorage()

sys.path.insert(1, './StockInfoPackage/')
import InfoManager as IM


with open("settings.json", "r") as file:
    data = json.loads(file.read())
    companies = data["companies"]
    mobilePlatforms = data["mobilePlatforms"]

'''
Helper functions for getting inforamtion
The function names are based on their type in the POST request
'''
def getCandlePlusQuote(stock: str, timeframe: str = "Y", quality:str = "high")->dict:
    data = IM.getQuote(stock)
    candleData = IM.getCandle(stock, timeframe, quality)
    data["prices"] = candleData["c"]
    data["dates"] = [time.ctime(t) for t in candleData["t"]]
    return data

def getCandle(stock: str, timeframe: str = "Y", quality:str = "high")->dict:
    stockData = IM.getCandle(stock, timeframe, quality)
    prices = stockData["c"]
    dates = [time.ctime(t) for t in stockData["t"]]
    data = {"prices":prices, "dates":dates}
    return data

def getQuote(stock: str)->dict:
    return IM.getQuote(request.form["name"])

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST": #POST
        # Web Security
        if not WebSecurity.validatePOST(request):
            return "Bad request. The server could not validate this POST request", 403 #Forbidden Request Status Code
        
        # Serve data to the request
        dataQuality = request.form.get("quality", "high")
        try: #These are put in a try except block in order to prevent crashing when bad post requests are sent
            if request.form["type"] == "quote+candle":
                if request.form["isMulti"] == 'true':
                    symbolData = {}
                    for symbol in json.loads(request.form["names"]):
                        symbolData[symbol] = getCandlePlusQuote(symbol, request.form["time"], dataQuality)
                    return symbolData
                else:
                    return getCandlePlusQuote(request.form["name"], request.form["time"], dataQuality)

            if request.form["type"] == "candle":
                return getCandle(request.form["name"], request.form["time"], dataQuality)

            if request.form["type"] == "quote":
                return getQuote(request.form["name"])

        except Exception as err:
            print("Internal Server Error: ", err)
            return "Internal Server Error", 500 #Internal Server Error Status Code
            
        except KeyError:
            pass

        return "Bad request. The request is missing required keys", 400 #Bad Request Status Code

    else:
        if request.user_agent.platform in mobilePlatforms:
            return redirect("/home/low")
        return redirect("/home/high")

@app.route("/home/<quality>", methods = ["GET"])
def indexWithQuality(quality):
    viewedStocks = companies
    response = ""
    workingQuality = quality if quality in ["high", "low"] else "high"

    if len(viewedStocks) > 10:
        response =  render_template("oneRequestIndex.html", stocks = viewedStocks, quality=workingQuality)
    else:
        response =  render_template("threadedRequestIndex.html", stocks = viewedStocks, quality=workingQuality)

    response = make_response(response)

    #Decide whether this request needs a new sessionID
    currentSessionID = request.cookies.get('sessionID', default="")
    if not WebSecurity.isSessionStored(currentSessionID):
        response.set_cookie("sessionID", WebSecurity.getNewSessionID())

    return response