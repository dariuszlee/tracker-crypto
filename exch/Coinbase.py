from json import load, loads, dump
from urllib.parse import urlencode

from tornado import ioloop, httpclient

import time
import datetime
from pprint import pprint

class CoinbaseExchange:
    __Data = None

    def __init__(self):
        if CoinbaseExchange.__Data == None:
            CoinbaseExchange.__Data = CoinbaseExchange.__loadData__()

    def get_price(self, currency, dateStr):
        url = self.__get_price_uri('priceSpot', currency, dateStr)
        client = httpclient.HTTPClient()
        httpmethod = "GET"
        request = httpclient.HTTPRequest(url, method=httpmethod)
        response = client.fetch(request)
        return loads(response.body)

    def __get_price_uri(self, endpoint, currency, date):
        query = urlencode({ 'date' : date})
        uri = self.__get_api_uri(endpoint)
        uri = uri.format(currency, query)
        print(uri)
        return uri


    def __get_api_uri(self, endpoint):
        return CoinbaseExchange.__Data['apiEndpoint'] + CoinbaseExchange.__Data[endpoint]

    def __loadData__():
        with open('api/exch-coinbase.json') as dataFile:
            data = load(dataFile)
            return data

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
    # cbExch = CoinbaseExchange()
    # data = cbExch.get_price('BTC-USD', '2018-01-02T01:02:51Z')
    # pprint(data)
    sweep_dates()
