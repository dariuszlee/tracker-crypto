from ExchangeInterface import ExchangeInterface

from tornado import ioloop, httpclient

from json import loads

class CoinbaseProExchange(ExchangeInterface):
    __Data = None

    def __init__(self):
        if CoinbaseProExchange.__Data == None:
            CoinbaseProExchange.__Data = self.__loadData__(self.get_exchname())

    def get_current_price(self, globalCurrency):
        localCurrency = self.get_local_exchange(globalCurrency, self.__Data)
        price = self.get_trades(localCurrency)[0].get('price')
        if price == None:
            return 0
        return price
        

    def get_trades(self, localCurrency):
        url = self.__get_trade_url('trades', localCurrency)
        return self.get_data(url)

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
    cbPro = CoinbaseProExchange()
    print(cbPro.get_current_price('btc-usd'))
