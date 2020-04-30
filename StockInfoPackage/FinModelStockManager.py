import requests
import json

def _datacutoff(data:dict, timeframe:str)->None:
    timeframeToCutoff = {
        "Y": 365,
        "M": -1,
        "W": -1,
        "D": -1
    }
    if timeframeToCutoff.get(timeframe, -1) != -1:
        cutoff = timeframeToCutoff.get(timeframe, -1)
        data['c'] = data['c'][-cutoff:]
        data['t'] = data['t'][-cutoff:]
    else:
        return

def makeDataSparse(data: dir, size:int):
    newC = []
    newT = []
    if len(data.get('c')) < size:
        return

    step = len(data.get('c')) // size

    for i in range(len(data.get('c'))):
        if i % step == 0:
            newC.append(data.get('c')[i])
            newT.append(data.get('t')[i])

    data['c'] = newC
    data['t'] = newT

def getCandle(symbol:str, timeframe: str="Y", quality:str="high", isCrypto=False):
    try:
        if timeframe=="Y":
            #return all historic data, but dont sparse it
            data = getAllHistoricData(symbol, "high", isSparse=False, isCrypto=isCrypto)
        else:
            data = getTimedHistoricData(symbol, timeframe)

    except Exception:
        return {}
    
    dataLength = 200 if quality=="high" else 50
    _datacutoff(data, timeframe)
    makeDataSparse(data, dataLength)
    
    return data

def getTimedHistoricData(symbol:str, timeframe:str)->dict:
    timeframeToUrl = {
        "M": "1hour", "W": "30min", "D":"15min"
    }

    url = "https://financialmodelingprep.com/api/v3/historical-chart/{}/{}".format(timeframeToUrl.get(timeframe, "1hour"), symbol)
    jsonData = requests.get(url).json()

    c = [day["close"] for day in jsonData[::-1]]
    t = [day["date"] for day in jsonData[::-1]]
    data = {'c': c, 't': t, 's': 'ok'}
    return data

def getAllHistoricData(symbol:str, quality='high', isSparse=True, isCrypto=False)->dict:
    isIndex = '^' in symbol

    if isIndex:
        url = 'https://financialmodelingprep.com/api/v3/historical-price-full/index/{}'.format(symbol)
    elif isCrypto:
        url = 'https://financialmodelingprep.com/api/v3/historical-price-full/crypto/{}'.format(symbol)
    else:
        url = "https://financialmodelingprep.com/api/v3/historical-price-full/{}?serietype=line".format(symbol)

    try:
        data = requests.get(url).json()
    except Exception:
        return {}

    c = [day["close"] for day in data['historical']]
    t = [day["date"] for day in data['historical']]

    if isIndex or isCrypto:
        c = c[::-1]
        t = t[::-1]
    
    dictData = {'c': c, 't': t, 's': 'ok'}

    if isSparse:
        makeDataSparse(dictData, 245 if quality == 'high' else 53)

    return dictData

def getQuote(symbol):
    url = "https://financialmodelingprep.com/api/v3/quote/{}".format(symbol)
    rawData = requests.get(url).json()

    if len(rawData) == 0:
        return {}
    else:
        rawData = rawData[0]

    data = {
        "current_price":rawData["price"],
        "difference": rawData["change"],
        "difference_percentage": rawData["changesPercentage"],
        "marketCap": rawData["marketCap"],
        "volume": rawData["volume"]
    }

    return data

def main():
    import matplotlib.pyplot as plt
    print(getQuote("BTCUSD"))
    # d = getCandle("BTCUSD", "D", "high", True)
    # plt.plot(d['c'])
    # plt.show()
    

if __name__ == "__main__":
    main()