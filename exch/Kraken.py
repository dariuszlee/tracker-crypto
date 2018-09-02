from json import load, loads, dump
from urllib.parse import urlencode

import time
import datetime
from pprint import pprint

from ExchangeInterface import ExchangeInterface

class KrakenExchange(ExchangeInterface):
    __Data = None

    def __init__(self):
        if KrakenExchange.__Data == None:
            KrakenExchange.__Data = self.__loadData__(self.get_exchname())
    
    # Current price will be the volume of the last one minute period
    def get_current_price(self, globalCurrency):
        localCurrency = self.get_local_exchange(globalCurrency, self.__Data)

        ohlc_data = self.get_ohlc(localCurrency, 1)
        last_ohlc = ohlc_data[len(ohlc_data) - 3]
        if last_ohlc[5] == 0.0:
            return last_ohlc[4]
        else:
            return last_ohlc[5]

    def get_ohlc(self, pair, interval, since = 0):
        url = self.__get_ohlc_url(pair, interval, since)
        response = self.get_data(url)
        if response['error'] == []:
            return response['result'][pair]
        else:
            return response['error']

    def get_trades(self, pair, since = 0):
        url = self.__get_trades_url(pair, since)
        return self.get_data(url)

    def __get_trades_url(self, pair, since):
        urlUnformated = self.get_url(self.__Data, 'tradesInfo')
        queryEncoded = urlencode({ 'pair' : pair, 'since' : since})
        url = urlUnformated.format(queryEncoded)
        return url

    def __get_ohlc_url(self, pair, interval = 1, since = 0):
        urlUnformated = self.get_url(self.__Data, 'ohlcInfo')
        queryEncoded = urlencode({ 'pair' : pair, 'interval' : interval, 'since' : since})
        url = urlUnformated.format(queryEncoded)
        return url

    def get_exchname(self):
        return 'kraken'


if __name__ == '__main__':
    kexch = KrakenExchange()

    timeDivision = 1000000000
    pair = 'XXBTZUSD'
    oneMinute = 1
    fiveMinute = 5

    print(kexch.get_current_price(pair))
