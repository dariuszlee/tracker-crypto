from json import load, loads, dump

from tornado import ioloop, httpclient

class ExchangeInterface:
    def __loadData__(self, exchName):
        path = "api/exch-{0}.json".format(exchName)
        with open(path) as dataFile:
            data = load(dataFile)
            return data

    def __exchname(self):
        raise NotImplementedError("Please implement exchange name")

    def get_data(self, url):
        client = httpclient.HTTPClient()
        httpmethod = "GET"
        request = httpclient.HTTPRequest(url, method=httpmethod)
        response = client.fetch(request)
        return loads(response.body)

    def get_url(self, data, endpoint):
        return data['apiEndpoint'] + data[endpoint]
