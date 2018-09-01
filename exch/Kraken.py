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
            KrakenExchange.__Data = self.__loadData__(self.__exchname())

    def get_ohlc(self, pair, interval, since = 0):
        url = self.__get_ohlc_url(pair, interval, since)
        return self.get_data(url)

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


    def __exchname(self):
        return 'kraken'


if __name__ == '__main__':
    kexch = KrakenExchange()

    timeDivision = 1000000000
    pair = 'XXBTZUSD'
    interval = 1440

    ohlcDataFromTrade = kexch.get_ohlc(pair, 1440)
    ohlcTradeDate = ohlcDataFromTrade['result'][pair][0][0]

    tradeData = kexch.get_trades(pair, ohlcTradeDate * timeDivision)
    tradeSince = tradeData['result']['last']
