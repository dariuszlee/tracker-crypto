from json import load, loads, dump

from tornado import ioloop, httpclient

class ExchangeInterface:
    def __init__(self, data):
        self.__Data = data

    def __loadData__(self, exchName):
        path = "api/exch-{0}.json".format(exchName)
        with open(path) as dataFile:
            data = load(dataFile)
            return data

    def get_exchname(self):
        raise NotImplementedError("Please implement exchange name.")

    def get_current_price(self, currency):
        raise NotImplementedError("Please implement get current price.")

    def get_local_exchange(self, globalCurrency, exchanges):
        exch = self.__Data['localExchanges'].get(globalCurrency)
        if exch == None:
            raise RuntimeError("Exchange:", globalCurrency, "not implemented in api-_.json")
        return exch

    def get_data(self, url):
        client = httpclient.HTTPClient()
        httpmethod = "GET"
        request = httpclient.HTTPRequest(url, method=httpmethod)
        response = client.fetch(request)
        return loads(response.body)

    def get_url(self, data, endpoint):
        return data['apiEndpoint'] + data[endpoint]
