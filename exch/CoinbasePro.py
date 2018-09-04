from ExchangeInterface import ExchangeInterface

from urllib.parse import urlencode
from tornado import ioloop, httpclient

from json import loads, dumps

from datetime import datetime, timedelta


class CoinbaseProExchange(ExchangeInterface):
    __Data = None

    def __init__(self):
        if CoinbaseProExchange.__Data == None:
            CoinbaseProExchange.__Data = self.__loadData__(self.get_exchname())
        super().__init__(self.__Data)

    def get_current_price(self, globalCurrency):
        localCurrency = self.get_local_exchange(globalCurrency)
        price = self.get_trades(localCurrency)[0].get('price')
        if price == None:
            return 0
        return price
        
    def get_price_at(self, currency, time):
        return 0

    def get_historical_dump(self):
        return 0

    def get_candles(self, currency, start = None, end = None, granularity = 60):
        localCurrency = self.get_local_exchange(currency)
        utcDiff = datetime.utcnow() - datetime.now()

        url = self.__get_candles_url(localCurrency, start, end, granularity)
        response = self.get_data(url)
        data = [ { 'time' : datetime.fromtimestamp(f[0]), 'close' : f[4], 'volume' : f[5] } for f in response ]
        # Verify dates
        if start != None and end != None:
            if data[-1]['time'] != end


    def get_trades(self, localCurrency):
        url = self.__get_trade_url('trades', localCurrency)
        return self.get_data(url)

    def get_server_time(self):
        url = self.get_url('time')
        return self.get_data(url)

    def __get_candles_url(self, cur, start, end, granularity):
        paramsToEncode = {}
        if start != None and end != None:
            paramsToEncode['start'] = start
            paramsToEncode['end'] = end 
        paramsToEncode['granularity'] = granularity
        paramsEncoded = urlencode(paramsToEncode)

        uri = self.get_url('candles')
        uri = uri.format(cur, paramsEncoded)
        return uri

    def __get_trade_url(self, endpoint, currency):
        uri = self.get_url(self.__Data, endpoint)
        uri = uri.format(currency)
        return uri

    def get_data(self, url):
        client = httpclient.HTTPClient()
        httpmethod = "GET"
        # Ugh... add Some user-agent. Api specific issue
        request = httpclient.HTTPRequest(url, method=httpmethod, headers={ 'user-agent' : 'tornado' })
        response = client.fetch(request)
        return loads(response.body)

    def get_exchname(self):
        return 'coinbase-pro'

if __name__ == '__main__':
    granularity = 3600
    currency = 'btc-usd'
    cbPro = CoinbaseProExchange()
    # print(cbPro.get_candles('btc-usd'))
    past = datetime(2018, 8, 22, 11, 0)
    pres = past + timedelta(seconds=granularity * 300)

    actualTime = pres - timedelta(seconds=granularity * 5)
    actualPast = past - timedelta(seconds=granularity * 5)
    data = cbPro.get_candles(currency, past.isoformat(), pres.isoformat(), granularity)
