import requests
import json


def makeDataSparse(data: dir, size:int):
    newC = []
    newT = []
    step = len(data.get('c')) // size

    for i in range(len(data.get('c'))):
        if i % step == 0:
            newC.append(data.get('c')[i])
            newT.append(data.get('t')[i])

    data['c'] = newC
    data['t'] = newT


def getAllHistoricData(symbol:str, quality='high')->dict:
    isIndex = '^' in symbol

    if isIndex:
        url = 'https://financialmodelingprep.com/api/v3/historical-price-full/index/{}'.format(symbol)
    else:
        url = "https://financialmodelingprep.com/api/v3/historical-price-full/{}?serietype=line".format(symbol)

    try:
        data = requests.get(url).json()
    except Exception:
        return {}

    c = [day["close"] for day in data['historical']]
    t = [day["date"] for day in data['historical']]

    if isIndex:
        print('INDEXXXXX')
        c = c[::-1]
        t = t[::-1]
    
    dictData = {'c': c, 't': t, 's': 'ok'}
    makeDataSparse(dictData, 245 if quality == 'high' else 53)

    return dictData

def main():
    print(len(getAllHistoricData('^IXIC', 'high').get('c')))

if __name__ == "__main__":
    main()