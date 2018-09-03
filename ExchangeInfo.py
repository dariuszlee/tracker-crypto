from exch.ExchangeAggregator import ExchangeAggregator

if __name__ == "__main__":
    print("Starting tracker")
    
    exchAggregator = ExchangeAggregator()
    supportedExchanges = exchAggregator.get_exchanges()
    while True:
        now = exchAggregator.get_now()
        for exch in now['exchanges']:
            print(now['date'])

