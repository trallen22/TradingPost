'''
This is a class for options, extended from the polygon_api
'''

from polygon_api import PolygonApi

class Option(PolygonApi):
    # TODO: need a way to reliable parse an option symbol
    def __init__(self, ticker):
        super().__init__
        self.ticker = ticker
        self.basicInfo = self.getBasicTickerInfo(ticker)
        self.extendedInfo = self.getExtendedTickerInfo(ticker)
        self.news = self.getTickerNews(ticker)
