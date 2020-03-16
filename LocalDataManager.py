import json
import DataValidator
import time


documentName = "localStorage.json"

def putData(symbol, data: dict) -> None:   
    '''
    Puts Data in the local storage if its not already there
    '''
    try:
        with open(documentName, "r") as file:
            readFile = file.read()
            if not len(readFile) == 0:
                currentData = json.loads(readFile)
            else:
                currentData = {}
    except FileNotFoundError:
        currentData = {}

    #Check if the symbol exists in the memory
    if symbol in currentData.keys():
        #Check if the data is already in the list
        for document in currentData[symbol]:
            #To check if no appending is requiered, check if the type and timeframe match, and make sure its not expierd
            if document["type"] == data["type"] and document["timeframe"] == data["timeframe"] and not DataValidator.isExpired(document):
                return
    else:
        currentData[symbol] = []

    #Puts an expiration date on the data
    DataValidator.putExpirationDate(data)

    with open(documentName, "w") as file:       
        currentData[symbol].append(data)
        file.write(json.dumps(currentData))

def getData(symbol, datatype: str, timeframe: str) -> dict:
    '''
    Gets data from the local storage\n
    If the data is not existent in the local storage, the function will return {}
    '''
    returndata = {}
    try:
        with open(documentName, "r") as file:
            currentData = json.loads(file.read())
            if symbol in currentData.keys():
                for document in currentData[symbol]:
                    if document["type"] == datatype and document["timeframe"] == timeframe and not DataValidator.isExpired(document):
                        returndata = document
    except FileNotFoundError:
        print("Local storge file not found")
    return returndata

def test():
    testData = {
        "prices" : [1,2,3,4,5],
        "type" : "candle",
        "timeframe" : "Y",
    }
    putData("GOOGL", testData)

if __name__ == "__main__":
    test()