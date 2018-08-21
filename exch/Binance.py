from json import load, loads, dump
from urllib.parse import urlencode

from tornado import ioloop, httpclient

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

    def get_symbol_data(self, symbol, dataPoints = 5):
        query = urlencode({'symbol' : symbol, 'limit' : dataPoints})
        url_template = BinanceExchange.__Data['apiEndpoint'] + BinanceExchange.__Data['dataInfo'] + "?{0}"
        url = url_template.format(query)
        print(url)
        client = httpclient.HTTPClient()
        httpmethod = "GET"
        request = httpclient.HTTPRequest(url, method=httpmethod)
        response = client.fetch(request)
        return loads(response.body)

    def __loadData__():
        with open('data/exch-binance.json') as dataFile:
            data = load(dataFile)
            return data

if __name__ == '__main__':
    binExch = BinanceExchange()
    data = binExch.get_symbol_data('BTCUSDT')
    print(data)
    # with open('data/binance-example.json', 'w') as f:
    #     dump(data, f)
