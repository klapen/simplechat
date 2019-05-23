import requests
import csv

class Bots:
    def getStockQuote(stock_code):
        print('StockCode: %s' % stock_code)
        url = 'https://stooq.com/q/l/?s=%s&f=sd2t2ohlcv&h&e=csv​'
        with requests.Session() as s:
            response = s.get(url % stock_code)
            if response.status_code != 200:
                print('Failed to get data:', response.status_code)
            else:
                data = csv.DictReader(response.text.strip().split('\n'))
                return '%s quote is $%s per share' % (stock_code.upper(), next(data)['Close'])
