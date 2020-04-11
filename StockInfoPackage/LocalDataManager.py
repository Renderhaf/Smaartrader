import json
import DataValidator as DV
import time


documentName = "localStorage.json"

def putData(symbol: str, data: dict) -> None:   
    """
    Puts Data in the local storage if its not already there
    """
    newdata = dict(data)
    try:
        with open(documentName, "r") as file:
            readFile = file.read()
            if not len(readFile) == 0:
                currentData = json.loads(readFile)
            else:
                currentData = {}
    except FileNotFoundError:
        currentData = {}
    except json.decoder.JSONDecodeError:
        clearCache()
        currentData = {}
    #Check if the symbol exists in the memory
    if symbol in currentData.keys():
        #Check if the data is already in the list
        for document in currentData[symbol]:
            #To check if no appending is required, check if the type and timeframe match
            if document["timeframe"] == data["timeframe"] and document["quality"] == data["quality"]:
                #The data is not expired
                if not DV.isExpired(document):
                    return
                else:
                    currentData[symbol].remove(document)
    else:
        currentData[symbol] = []

    #Puts an expiration date on the data
    DV.putExpirationDate(newdata)

    with open(documentName, "w") as file:       
        currentData[symbol].append(newdata)
        file.write(json.dumps(currentData))

def getData(symbol, timeframe: str,quality:str='high') -> dict:
    """
    Gets data from the local storage\n
    If the data does not exist in the local storage, the function will return {}
    """
    returndata = {}
    try:
        with open(documentName, "r") as file:
            currentData = json.loads(file.read())
            if symbol in currentData.keys():
                for document in currentData[symbol]:
                    if document["timeframe"] == timeframe and document["quality"] == quality and not DV.isExpired(document):
                        returndata = document
    except FileNotFoundError:
        print("Local storge file not found")
    except json.decoder.JSONDecodeError:
        clearCache()
        print("Local storge file repaired")
    return returndata

def clearCache()->None:
    with open(documentName, "w") as file:       
        file.write('{}')


def test():
    testData = {
        "prices" : [1,2,3,4,5],
        "timeframe" : "Y",
    }
    putData("AAPL", testData)

if __name__ == "__main__":
    test()