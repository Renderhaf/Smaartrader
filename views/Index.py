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
 Helper Functions
'''
def getCategory(name: str) -> list:
    if name in categories.keys():
        return categories.get(name)
    else:
        return categories.get("IT")


def getViewableName(ticker: str, maxLength=13) -> str:
    rawName = IM.getName(ticker)
    splitName = rawName.split(" ")
    for i in range(len(splitName)-1):
        if len(" ".join(splitName)) > maxLength:
            splitName.pop()
    return " ".join(splitName)


@app.route("/", methods=["GET"])
def index():
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
