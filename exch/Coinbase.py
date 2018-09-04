from ExchangeInterface import ExchangeInterface

from json import load, loads, dump
from urllib.parse import urlencode

from tornado import ioloop, httpclient

import time
import datetime
from pprint import pprint

class CoinbaseExchange(ExchangeInterface):
    __Data = None

    def __init__(self):
        if CoinbaseExchange.__Data == None:
            CoinbaseExchange.__Data = self.__loadData__(self.get_exchname())

    def get_current_price(self, globalCurrency):
        localCurrency = self.get_local_exchange(globalCurrency, self.__Data)

        price = self.get_price(localCurrency).get('data')
        if price != None:
            return price.get('amount')
        else:
            return price

    def get_price(self, currency, dateStr = None):
        url = self.__get_price_uri('priceSpot', currency, dateStr)
        return self.get_data(url)

    def get_historical_dump(self):

    def get_sell_price(self, currency, dateStr = None):
        url = self.__get_price_uri('sellPrice', currency, dateStr)
        return self.get_data(url)

    def get_buy_price(self, currency, dateStr = None):
        url = self.__get_price_uri('buyPrice', currency, dateStr)
        return self.get_data(url)

    def __get_price_uri(self, endpoint, currency, date):
        if date == None:
            query = ""
        else:
            query = urlencode({ 'date' : date})
        uri = self.__get_api_uri(endpoint)
        uri = uri.format(currency, query)
        return uri


    def __get_api_uri(self, endpoint):
        return CoinbaseExchange.__Data['apiEndpoint'] + CoinbaseExchange.__Data[endpoint]

    def get_exchname(self):
        return 'coinbase'

def sweep_dates():
    coinbaseExch = CoinbaseExchange()
    minusDay = datetime.timedelta(days=1)

    currDay = datetime.date(2010, 7, 18)
    currDayStr = str(currDay)
    data = coinbaseExch.get_price('BTC-USD', currDayStr)
    while data != None:
        currDay = currDay - minusDay
        currDayStr = str(currDay)

        data = coinbaseExch.get_price('BTC-USD', currDayStr)
        print(data)
        if data['data']['amount'] == '0.00':
            break


if __name__ == '__main__':
    cbExch = CoinbaseExchange()
    data = cbExch.get_price('btc-usd', '2018-01-01T02:02:00Z')
    sellPrice = cbExch.get_sell_price('btc-usd', '2018-01-01T02:02:00Z')
    buyPrice = cbExch.get_buy_price('btc-usd', '2018-01-01T02:02:00Z')
    print(data)
    print("Sell:", sellPrice)
    print("Buy:", buyPrice)
