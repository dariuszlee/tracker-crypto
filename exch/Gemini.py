from ExchangeInterface import ExchangeInterface

from urllib.parse import urlencode

class GeminiExchange(ExchangeInterface):
    __Data = None
    def __init__(self):
        if GeminiExchange.__Data == None:
            GeminiExchange.__Data = self.__loadData__(self.get_exchname())

    def get_current_price(self, globalCurrency):
        localCurrency = self.get_local_exchange(globalCurrency, self.__Data)
        response = self.get_trades(localCurrency) 
        price = response[0].get('price')
        if price == None:
            return 0
        return price

    def get_trades(self, localCurrency, numTrades = 1):
        url = self.__get_trade_url('tradesInfo', localCurrency, numTrades)
        return self.get_data(url)

    def __get_trade_url(self, endpoint, currency, numTrades):
        queryEncoded = urlencode({ 'limit_trades' : numTrades })
        uri = self.get_url(self.__Data, endpoint)
        uri = uri.format(currency, queryEncoded)
        return uri

    def get_exchname(self):
        return 'gemini'

if __name__ == '__main__':
    cbPro = GeminiExchange()
    print(cbPro.get_current_price('btc-usd'))
