import requests
import json

def getAllHistoricData(symbol, quality='high'):
    url = "https://financialmodelingprep.com/api/v3/historical-price-full/{}?serietype=line".format(symbol)
    try:
        data = requests.get(url).json()
    except Exception:
        return {}

    c = [day["close"] for day in data['historical']]
    t = [day["date"] for day in data['historical']]
    
    return {'c': c, 't': t}

def main():
    print(getAllHistoricData('AAPL'))

if __name__ == "__main__":
    main()