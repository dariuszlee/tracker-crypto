from json import load

from Binance import BinanceExchange
from Coinbase import CoinbaseExchange
from Kraken import KrakenExchange
from CoinbasePro import CoinbaseProExchange
from Gemini import GeminiExchange

class ExchangeAggregator:
    Data = None

    def __init__(self):
        self.__exchanges__ = [
            BinanceExchange(),
            GeminiExchange(),
            CoinbaseProExchange(),
            KrakenExchange()
        ]
        self.Data = self.__load_data()

    def get_now(self, currency):
        return [ { f.get_exchname() : f.get_current_price(currency) } for f in self.__exchanges__]

    def get_at_time(self, currency, time):
        return [ { f.get_exchname() : f.get_price_at(currency, time) } for f in self.__exchanges__]

    def get_exchanges(self):
        return [ f.get_exchname() for f in self.__exchanges__]

    def __load_data(self):
        with open('api/exch-aggregator.json') as f:
            return load(f)

def get_dated():
    pass


if __name__ == '__main__':
    exchAggregator = ExchangeAggregator()
    print(exchAggregator.get_now('btc-usd'))

