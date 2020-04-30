from server import app
import sys
from flask import make_response, render_template, request
import json

sys.path.insert(1, './StockInfoPackage/')
import StockInfoPackage.InfoManager as IM
import StockInfoPackage.StockAnalysisManager as SI

import WebSecurity

@app.route("/stock/<stockname>", methods=['GET'])
def singleStockPage(stockname):
    #Make sure the stockname is a valid stock name
    if WebSecurity.checkForSpecialChars(stockname) or not IM.isAnExistingTicker(stockname):
        return "<h1>That is not a valid stock ticker</h1>"

    closeData = IM.getCandle(stockname, timeframe="Y", quality="high").get("c")

    stockTrend = SI.getCurrentTrend(stockname, closeData=closeData)

    sampleSize = 25

    historicSMA = SI.getHistoricSMA(stockname, sampleSize , closeData=closeData)
    currentSMA = round(historicSMA[-1],2)

    historicEMA, stockPrice = SI.getHistoricEMA(stockname, sampleSize, True, closeData=closeData)
    currentEMA = round(historicEMA[-1],2)

    # Indicator Name | Indicator Value | is Indicator giving a positive view

    indicators = [["Trend (10 Days)", stockTrend, stockTrend > 0], 
                    ["SMA (25 Days)", currentSMA, currentSMA < stockPrice],
                    ["EMA (25 Days)", currentEMA, currentEMA < stockPrice]]

    #These are indicator graphs for use in the browser [Graph Name | Graph data (JSON) | Graph Delay]
    graphs = [["EMA", json.dumps(historicEMA), sampleSize],
                ["SMA", json.dumps(historicSMA), sampleSize]]
                
    response = make_response(render_template("singleStockPage.html", stock = stockname,
                                                                    quality="high",
                                                                    name=" ".join(IM.getName(stockname).split(" ")[:2]),
                                                                    wikiarticle=SI.getWikiArticle(stockname),
                                                                    indicators=indicators,
                                                                    graphs=graphs))

    #Decide whether this request needs a new sessionID
    currentSessionID = request.cookies.get('sessionID', default="")
    if not WebSecurity.isSessionStored(currentSessionID):
        response.set_cookie("sessionID", WebSecurity.getNewSessionID())

    return response

@app.route("/searchStock", methods=['POST'])
def searchStock():
    response = dict()
    stockTicker = request.form.get("searchStock")

    if WebSecurity.checkForSpecialChars(stockTicker) or not IM.isAnExistingTicker(stockTicker):
        response["type"] = "alert"
        response["data"] = "That is not a valid stock ticker"
    else:
        response["type"] = "link"
        response["data"] = "/stock/"+stockTicker
    return response