import secrets
from flask import request as flask_request
import time
import json

storeLocation = "./sessionStorage.json"
sessionLifetime = 12 * 60 * 60 #12 hours

def getNewSessionID()->str:
    token = secrets.token_hex(32)
    storeToken(token)
    return token

def validatePOST(request: flask_request)->bool:
    return isSessionStored(request.cookies.get("sessionID"))

def resetStorage()->None:
    with open(storeLocation, "w") as file:
        file.write("")

def storeToken(token:str)->None:
    storage = getSessionStorage()

    expirationTime = time.time() + sessionLifetime
    storage[token] = {"expiration": expirationTime}

    with open(storeLocation, "w") as file:
        file.write(json.dumps(storage))

def isSessionStored(sessionID: str)->bool:
    storage = getSessionStorage()
    currentTime = time.time()
    if sessionID in storage.keys():
        #Check expiration, and if expired, erase the sessionID
        if storage[sessionID]["expiration"] < currentTime:
            del storage[sessionID]
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

if __name__ == "__main__":
    print(getSessionID())