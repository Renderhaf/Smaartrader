from server import app
import sys
from flask import make_response, render_template, request

sys.path.insert(1, './StockInfoPackage/')
import InfoManager as IM
import StockAnalysisManager as SI

import WebSecurity

@app.route("/stock/<stockname>", methods=['GET'])
def singleStockPage(stockname):
    #Make sure the stockname is a valid stock name
    if WebSecurity.checkForSpecialChars(stockname) or not IM.isAnExistingTicker(stockname):
        return "<h1>That is not a valid stock ticker</h1>"

    stockTrend = SI.getCurrentTrend(stockname)

    sampleSize = 25
    currentSMA, stockPrice = SI.getCurrentSMA(stockname, sampleSize, returnPrice=True)
    currentEMA = SI.getCurrentEMA(stockname, sampleSize)

    # Indicator Name | Indicator Value | is Indicator giving a positive view

    indicators = [["Trend (10 Days)", stockTrend, stockTrend > 0], 
                    ["SMA (25 Days)", currentSMA, currentSMA < stockPrice],
                    ["EMA (25 Days)", currentEMA, currentEMA < stockPrice]]

    response = make_response(render_template("singleStockPage.html", stock = stockname,
                                                                    quality="high",
                                                                    name=IM.getName(stockname),
                                                                    wikiarticle=SI.getWikiArticle(stockname),
                                                                    indicators=indicators))

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