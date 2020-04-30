import pytest
import requests
import json
import sys

sys.path.insert(1, './StockInfoPackage/')

import FinnhubStockManager as SM
import DatabaseManager as DM
import InfoManager as IM
import LocalDataManager as LM
import WebSecurity as WS

'''
Test helpers
'''

GENERIC_STOCK_NAME = 'AAPL'
RARE_STOCK_NAME = 'GM'

def about_equals(val_a, val_b, errorRange = 0.1):
    return abs(val_a - val_b) < errorRange

'''
StockManager Tests
'''
def test_quote():
    assert len(SM.getQuote(GENERIC_STOCK_NAME).keys()) != 0

def test_candle():
    assert len(SM.getCandle(GENERIC_STOCK_NAME).keys()) != 0

'''
DatabaseManager Tests
'''
def test_store_db():
    candle = SM.getCandle(RARE_STOCK_NAME)
    candle["timeframe"] = "Y"
    candle["quality"] = "high"

    isStore = True
    try:
        DM.storeData(RARE_STOCK_NAME, candle)
    except:
        isStore = False

    assert isStore

def test_get_db():
    data = DM.getData(RARE_STOCK_NAME, "Y").keys()
    assert len(data) != 0

def test_delete_db():
    isDelete = True
    try:
        DM.removeData(RARE_STOCK_NAME, "Y")
    except:
        isDelete = False

    assert isDelete

'''
LocalDataManager Tests
'''
def test_store_ls():
    candle = SM.getCandle(RARE_STOCK_NAME)
    candle["timeframe"] = "Y"
    candle["quality"] = "high"

    isStore = True
    try:
        LM.putData(RARE_STOCK_NAME, candle)
    except:
        isStore = False

    assert isStore

def test_get_ls():
    data = LM.getData(RARE_STOCK_NAME, "Y").keys()
    assert len(data) != 0

'''
Web Security Tests
'''

zero_token = WS.getNewSessionID(0)
good_token = WS.getNewSessionID()

def test_session_token():
    #Create a session with no lifetime
    assert type(zero_token) == str 
    assert len(zero_token) > 10

def test_session_lifetime():
    assert not WS.isSessionStored(zero_token)
    assert WS.isSessionStored(good_token)

def test_clean_session_memory():
    WS.resetStorage()
    assert not WS.isSessionStored(good_token)