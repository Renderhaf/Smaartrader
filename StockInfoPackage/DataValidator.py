import time

"""
This is a dictionary that defines the amount of time every item has until its spoiled in hours
Y - Yearly Candle
M - Monthly Candle
W - Weekly Candle
Q - Quote
"""
spoilTimes = {"Y": 30, "M": 30, "W": 10, "Q": 0.5,'D':0.1}
expirationDateKey = "expirationDate"
spoilTimeConversion = 3600

def isExpired(data : dict):
    """
    Returns whether the data is expired or not
    """
    try:
        expiredStatus = int(data[expirationDateKey]) < int(time.time())
    except KeyError:
        return True
    return expiredStatus

def putExpirationDate(data: dict) -> None:
    """
    Mutates the dict so that it has a correct expiration date
    """
    try:
        expirationDiff = spoilTimes[data["timeframe"]] * spoilTimeConversion
    except KeyError:
        print("The data does not have a timeframe, cannot put an expiration date on it.")
        return
    data[expirationDateKey] = int(time.time()) + int(expirationDiff)


def test():
    data = {"prices": [0,1,2,3,4], "timeframe": "Y"}
    putExpirationDate(data)
    print(time.ctime(data[expirationDateKey]), isExpired(data))

if __name__ == "__main__":
    test()
