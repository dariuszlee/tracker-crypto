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

        super().__init__(KrakenExchange.__Data)
    
    # Current price will be the volume of the last one minute period
    def get_current_price(self, globalCurrency):
        localCurrency = self.get_local_exchange(globalCurrency, self.__Data)

        last_trades = self.get_trades(localCurrency)
        most_recent_trade = last_trades[len(last_trades) - 1]
        return most_recent_trade[0]

    def get_ohlc(self, pair, interval, since = 0):
        url = self.__get_ohlc_url(pair, interval, since)
        response = self.get_data(url)
        if response['error'] == []:
            return response['result'][pair]
        else:
            return response['error']

    def get_trades(self, pair, since = None):
        url = self.__get_trades_url(pair, since)
        response = self.get_data(url)
        if response['error'] == []:
            return response['result'][pair]
        else:
            return response['error']
        return d

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
    pair = 'btc-usd'
    oneMinute = 1
    fiveMinute = 5

    localPair = kexch.get_local_exchange(pair, None)

    print(kexch.get_trades(localPair))
    print(kexch.get_current_price(pair))
