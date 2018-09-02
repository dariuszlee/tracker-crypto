from ExchangeInterface import ExchangeInterface

from json import load, loads, dump
from urllib.parse import urlencode

from tornado import ioloop, httpclient

import time
import datetime
from pprint import pprint

def Dump_Historical():
    binExch = BinanceExchange()

    earliestTime = binExch.get_earliest_time()
    earliestDate = BinanceExchange.ms_to_datetime(earliestTime)

    currentTime = int(time.time() * 1000)
    currentDate = BinanceExchange.ms_to_datetime(currentTime)

    print("First date:", earliestDate, "Current date:", currentDate)
    dateDiff = currentDate - earliestDate
    print("Date Diff is:", dateDiff.days, "and in hours", dateDiff.seconds / 3600)

    data = binExch.get_kline_info('BTCUSDT', '1d', 1000, earliestTime)
    print("Num of points:", len(data))
    print("Last point is: ", data[len(data) - 1])
    print("Last point is: ", data[0])

def Get_Exchange_Data():
    binExch = BinanceExchange()
    exchDat = binExch.get_exchange_data()
    pprint(exchDat)

class BinanceExchange(ExchangeInterface):
    __Data = None

    def __init__(self):
        if BinanceExchange.__Data == None:
            BinanceExchange.__Data = self.__loadData__(self.get_exchname())

    def get_earliest_time(self):
        return BinanceExchange.__Data['earliestTimeInMs']

    def get_current_price(self, globalCurrency):
        localCurrency = self.get_local_exchange(globalCurrency, self.__Data)
        
        currentKline = self.get_kline_info(localCurrency, '1m', 1)[0]
        return currentKline.get('close')

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

    def get_kline_info(self, symbol, interval, points = 500, startTime = None):
        if startTime == None:
            queryData = { 'symbol' : symbol, 'interval': interval, 'limit' : points }
        else:
            queryData = { 'symbol' : symbol, 'interval': interval, 'limit' : points, 'startTime': startTime}
        url = self.__create_api_uri('klineInfo', queryData)
        client = httpclient.HTTPClient()
        httpmethod = "GET"
        request = httpclient.HTTPRequest(url, method=httpmethod)
        response = client.fetch(request)
        return [ { 
                    'startDate' : BinanceExchange.ms_to_datetime(f[0]),
                    'close' : f[4],
                    'endDate' : BinanceExchange.ms_to_datetime(f[6])
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

    def get_exchname(self):
        return 'binance'

if __name__ == '__main__':
    binExch = BinanceExchange()
    data = binExch.get_kline_info('BTCUSDT', '1m', 1)
    print(data)
