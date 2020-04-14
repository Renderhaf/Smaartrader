import secrets
from flask import request as flask_request
import time
import json

storeLocation = "./sessionStorage.json"
sessionLifetime = 12 * 60 * 60 #12 hours

normalCharsKey = "abcdefghijklmnopqrstuvwxyz0123456789-.^"

def getNewSessionID(lifetime: int = sessionLifetime)->str:
    token = secrets.token_hex(32)
    storeToken(token, lifetime)
    return token

def validatePOST(request: flask_request)->bool:
    return isSessionStored(request.cookies.get("sessionID"))

def resetStorage()->None:
    with open(storeLocation, "w") as file:
        file.write("{}")

def storeToken(token:str, lifetime:int = sessionLifetime)->None:
    storage = getSessionStorage()

    expirationTime = time.time() + lifetime
    storage[token] = {"expiration": expirationTime}

    with open(storeLocation, "w") as file:
        file.write(json.dumps(storage))

def isSessionStored(sessionID: str)->bool:
    storage = getSessionStorage()
    currentTime = time.time()
    if sessionID in storage.keys():
        #Check expiration, and if expired, erase the sessionID
        if storage[sessionID]["expiration"] < currentTime:
            storage.pop(sessionID)
            with open(storeLocation, "w") as file:
                file.write(json.dumps(storage))
            return False

        return True

    return False

def getSessionStorage()->dict:
    storage = dict()

    try:
        with open(storeLocation, "r") as file:
            storage = json.loads(file.read())
    except:
        resetStorage()
    return storage

def checkForSpecialChars(text:str, key=normalCharsKey)->bool:
    for char in text:
        if char.lower() not in key:
            return True
    return False

if __name__ == "__main__":
    print(getNewSessionID())