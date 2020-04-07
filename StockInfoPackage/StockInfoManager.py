import json
import requests
with open("./DataFiles/stockTickers.json", "r") as file:
    tickers = json.loads(file.read())

def getName(ticker:str)->str:
    return tickers.get(ticker, ticker)

def getWikiArticle(ticker: str)->str:
    name = getName(ticker)
    if name == ticker:
        quary = "Stock Market"
    else:
        quary = name
    url = 'https://en.wikipedia.org/w/api.php?action=opensearch&search="{}"&limit=1&format=json'.format(quary)
    return requests.get(url).json()[-1][0]

def main():
    print(getWikiArticle("GOOG"))

if __name__ == "__main__":
    main()