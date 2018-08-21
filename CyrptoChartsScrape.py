from tornado import ioloop, httpclient
import lxml.html
import lxml.etree

from functools import partial

def handle_response(response):
    print("Retrieved")
    html = lxml.html.fromstring(response.body)
    html = html.xpath("//div[@class='d_row panel-group']/div[@class='name_td']/a")
    for e in html:
        href = e.get('href')
        print(href)
        # print(lxml.html.tostring(e))
    # afterSelect = html.cssselect('.d_row.panel_group')
    # print(afterSelect.tostring())
    ioloop.IOLoop.instance().stop()

def initiate_get():
    print("Starting get")
    url = 'https://cryptocoincharts.info/markets/info'
    client = httpclient.AsyncHTTPClient()
    httpmethod = "GET"
    request = httpclient.HTTPRequest(url, method=httpmethod)
    client.fetch(request, partial(handle_response))

def main():
    initiate_get()
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
