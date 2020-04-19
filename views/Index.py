from server import app
from flask import request, render_template, redirect, make_response
import time
import sys
import json

import WebSecurity
WebSecurity.resetStorage()

sys.path.insert(1, './StockInfoPackage/')
import StockInfoPackage.InfoManager as IM


with open("settings.json", "r") as file:
    data = json.loads(file.read())
    categories: dict = data["categories"]
    mobilePlatforms = data["mobilePlatforms"]

'''
Helper functions for getting inforamtion
The function names are based on their type in the POST request
'''
def cleanDataFromObjectID(data: dict):
    for i in data.keys():
        if type(data[i]) == 'ObjectId':
            del data[i]

def getCandlePlusQuote(stock: str, timeframe: str = "Y", quality: str = "high") -> dict:
    data = IM.getQuote(stock)
    candleData = IM.getCandle(stock, timeframe, quality)
    data["prices"] = candleData["c"]
    data["dates"] = [time.ctime(t) for t in candleData["t"]]

    #This should not be here but this bug is driving me insane
    cleanDataFromObjectID(data)
            
    return data


def getCandle(stock: str, timeframe: str = "Y", quality: str = "high") -> dict:
    stockData = IM.getCandle(stock, timeframe, quality)
    prices = stockData["c"]
    dates = [time.ctime(t) for t in stockData["t"]]
    data = {"prices": prices, "dates": dates}

    return data


def getQuote(stock: str) -> dict:
    return IM.getQuote(request.form["name"])


def getViewableName(ticker: str, maxLength=13) -> str:
    rawName = IM.getName(ticker)
    splitName = rawName.split(" ")
    for i in range(len(splitName)-1):
        if len(" ".join(splitName)) > maxLength:
            splitName.pop()
    return " ".join(splitName)


def getCategory(name: str) -> list:
    if name in categories.keys():
        return categories.get(name)
    else:
        return categories.get("IT")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":  # POST
        # Web Security
        if not WebSecurity.validatePOST(request):
            # Forbidden Request Status Code
            return "Bad request. The server could not validate this POST request", 403

        # Serve data to the request
        dataQuality = request.form.get("quality", "high")
        try:  # These are put in a try except block in order to prevent crashing when bad post requests are sent
            if request.form["type"] == "quote+candle":
                if request.form["isMulti"] == 'true':
                    symbolData = {}
                    for symbol in json.loads(request.form["names"]):
                        symbolData[symbol] = getCandlePlusQuote(
                            symbol, request.form["time"], dataQuality)
                    return symbolData
                else:
                    return getCandlePlusQuote(request.form["name"], request.form["time"], dataQuality)

            if request.form["type"] == "candle":
                return getCandle(request.form["name"], request.form["time"], dataQuality)

            if request.form["type"] == "quote":
                return getQuote(request.form["name"])

        except Exception as err:
            print("Internal Server Error: ", err)
            return "Internal Server Error", 500  # Internal Server Error Status Code

        except KeyError:
            pass

        # Bad Request Status Code
        return "Bad request. The request is missing required keys", 400

    else:
        if request.user_agent.platform in mobilePlatforms:
            return redirect("/home?quality=low")
        return redirect("/home?quality=high")


@app.route("/home/", methods=["GET"])
def indexWithQuality():
    quality = request.args.get("quality", default="high")
    category = request.args.get("category", default="IT")

    viewedStocks = getCategory(category)
    viewedStockNames = [getViewableName(ticker) for ticker in viewedStocks]

    response = ""
    workingQuality = quality if quality in ["high", "low"] else "high"

    otherCategories = list(categories.keys())
    otherCategories.remove(category)

    response = render_template("threadedRequestIndex.html", stocks=viewedStocks,
                               quality=workingQuality, delayStep=200, stocknames=viewedStockNames, selectedCategory=category, otherCategories = otherCategories)

    response = make_response(response)

    # Decide whether this request needs a new sessionID
    currentSessionID = request.cookies.get('sessionID', default="")
    if not WebSecurity.isSessionStored(currentSessionID):
        response.set_cookie("sessionID", WebSecurity.getNewSessionID())

    return response
