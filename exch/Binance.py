from json import load, loads, dump
from urllib.parse import urlencode

from tornado import ioloop, httpclient

import time
import datetime
from pprint import pprint

class BinanceExchange:
    __Data = None

    def __init__(self):
        if BinanceExchange.__Data == None:
            BinanceExchange.__Data = BinanceExchange.__loadData__()

    def get_exchange_data(self):
        url = BinanceExchange.__Data['apiEndpoint'] + BinanceExchange.__Data['exchInfo']
        client = httpclient.HTTPClient()
        httpmethod = "GET"
        request = httpclient.HTTPRequest(url, method=httpmethod)
        response = client.fetch(request)
        return loads(response.body)

    def get_symbol_bids(self, symbol, dataPoints = 5):
        queryData = {'symbol' : symbol, 'limit' : dataPoints}
        url = self.__create_api_uri('orderInfo', queryData)
        client = httpclient.HTTPClient()
        httpmethod = "GET"
        request = httpclient.HTTPRequest(url, method=httpmethod)
        response = client.fetch(request)
        return loads(response.body)

    def get_aggregate_info(self, symbol, startTime):
        queryData = { 'symbol' : symbol, 'startTime': startTime }
        url = self.__create_api_uri('aggregateInfo', queryData)
        client = httpclient.HTTPClient()
        httpmethod = "GET"
        request = httpclient.HTTPRequest(url, method=httpmethod)
        response = client.fetch(request)
        return loads(response.body)

    def get_server_time(self):
        url = self.__create_api_uri('serverTime')
        client = httpclient.HTTPClient()
        httpmethod = "GET"
        request = httpclient.HTTPRequest(url, method=httpmethod)
        response = client.fetch(request)
        return loads(response.body)

    def get_kline_info(self, symbol, interval, points, startTime):
        queryData = { 'symbol' : symbol, 'interval': interval, 'limit' : points, 'startTime': startTime}
        url = self.__create_api_uri('klineInfo', queryData)
        client = httpclient.HTTPClient()
        httpmethod = "GET"
        request = httpclient.HTTPRequest(url, method=httpmethod)
        response = client.fetch(request)
        return [ { 
                    'startDate' : BinanceExchange.ms_to_datetime(f[0])
                 }
                for f in loads(response.body) 
                ]


    def __create_api_uri(self, endpoint, queryData = None):
        if queryData != None:
            queryStr = urlencode(queryData)
            endpointInfo = BinanceExchange.__Data[endpoint] + "?{0}"
            endpointInfo = endpointInfo.format(queryStr)
        else:
            endpointInfo = BinanceExchange.__Data[endpoint]
        
        url = BinanceExchange.__Data['apiEndpoint'] + endpointInfo

        print(url)
        return url

    def ms_to_datetime(timeInMs):
        return datetime.datetime.fromtimestamp(timeInMs / 1000)


    def __loadData__():
        with open('api/exch-binance.json') as dataFile:
            data = load(dataFile)
            return data

if __name__ == '__main__':
    binExch = BinanceExchange()
    # data = binExch.get_aggregate_info('BTCUSDT', myTime)
    data = binExch.get_server_time()
    time = data['serverTime'] - (1000 * 60 * 60 * 24 * 365 * 20)
    # time = data['serverTime']
    data = binExch.get_kline_info('BTCUSDT', '1M', 16, time)
    pprint(data)
    print("Points of data", len(data))
    # date = datetime.datetime.fromtimestamp(time / 1000)
    # pprint(data)
    # with open('data/binance-example.json', 'w') as f:
    #     dump(data, f)
