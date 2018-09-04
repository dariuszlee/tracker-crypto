from ExchangeInterface import ExchangeInterface

from urllib.parse import urlencode

class BitstampExchange(ExchangeInterface):
    __Data = None
    __DefaultDateParams = set(['minute', 'hour', 'day'])

    def __init__(self):
        if BitstampExchange.__Data == None:
            BitstampExchange.__Data = self.__loadData__(self.get_exchname())
        super().__init__(self.__Data)

    def get_current_price(self, globalCurrency):
        localCurrency = self.get_local_exchange(globalCurrency)
        response = self.get_trades(localCurrency) 
        print(len(response))
        price = response[0].get('price')
        if price == None:
            return 0
        return price

    def get_trades(self, localCurrency, dateParam = 'hour'):
        if dateParam not in BitstampExchange.__DefaultDateParams:
            raise KeyError('Provided date param not supported:', dateParam)
        url = self.__get_trade_url('tradesInfo', localCurrency, dateParam)
        return self.get_data(url)

    def __get_trade_url(self, endpoint, currency, dateParam):
        encoded = urlencode({ 'time' : dateParam })
        uri = self.get_url(endpoint)
        uri = uri.format(currency, encoded)
        return uri

    def get_exchname(self):
        return 'bitstamp'

if __name__ == '__main__':
    cbPro = BitstampExchange()
    print(cbPro.get_current_price('btc-usd'))
