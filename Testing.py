import unittest
import requests
import json
import sys

sys.path.insert(1, './StockInfoPackage/')

import StockManager as SM
import DataValidator as DV
import DatabaseManager as DM
import InfoManager as IM
import LocalDataManager as LM


class TestDV(unittest.TestCase):
    pass
class TestDM(unittest.TestCase):
    pass
class TestIM(unittest.TestCase):
    pass
class TestLM(unittest.TestCase):
    pass


class TestSM(unittest.TestCase):

    def test_raw_quote(self):
        self.assertEqual(SM.getRawQuote('AAPL'),requests.get('https://finnhub.io/api/v1/quote?symbol=AAPL&token=bpml3jvrh5rf2as807og').json())
        self.assertEqual(SM.getRawQuote('INC'),requests.get('https://finnhub.io/api/v1/quote?symbol=INC&token=bpml3jvrh5rf2as807og').json())
        self.assertEqual(SM.getRawQuote('GOOGL'),requests.get('https://finnhub.io/api/v1/quote?symbol=GOOGL&token=bpml3jvrh5rf2as807og').json())
        #should raise error if symbol is not str
        with self.assertRaises(TypeError):
            SM.getRawQuote(12)
        
    def test_raw_candle(self):
        self.assertEqual(SM.getRawCandle('AAPL'),requests.get('https://finnhub.io/api/v1/stock/candle?symbol=AAPL&resolution=D&count=365&token=bpml3jvrh5rf2as807og').json())
        self.assertEqual(SM.getRawCandle('GOOGL','D'),requests.get('https://finnhub.io/api/v1/stock/candle?symbol=GOOGL&resolution=D&count=365&token=bpml3jvrh5rf2as807og').json())
        self.assertEqual(SM.getRawCandle('INC','W',50),requests.get('https://finnhub.io/api/v1/stock/candle?symbol=INC&resolution=W&count=50&token=bpml3jvrh5rf2as807og').json())
        self.assertEqual(SM.getRawCandle('AAPL',12),{})       
        #should raise error
        with self.assertRaises(TypeError):
            SM.getRawCandle()

if __name__ == '__main__':
    unittest.main()