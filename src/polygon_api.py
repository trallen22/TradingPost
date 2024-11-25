import requests
from datetime import datetime
import configuration_file as config

class PolygonApi():
    _POLYGON_API_ENDPOINT = "https://api.polygon.io"
    _POLYGON_API_KEY = "CP1nN_q8W8C4eG7phIPNgLNCyPEyDZPe" # free version 

    @classmethod
    def makeGetRequest(cls, apiEndpoint):
        # need to check if '?' is in apiEndpoint to allow the apiKey to be added to the end
        if ("?" not in apiEndpoint):
            apiEndpoint = f"{apiEndpoint}?"
        return requests.get(f"{cls._POLYGON_API_ENDPOINT}{apiEndpoint}&apiKey={cls._POLYGON_API_KEY}")

    @classmethod
    def getBasicTickerInfo(cls, ticker):
        return cls.makeGetRequest(f"/v3/reference/tickers?ticker={ticker}")

    @classmethod
    def getExtendedTickerInfo(cls, ticker):
        return cls.makeGetRequest(f"/v3/reference/tickers/{ticker}")

    @classmethod
    def getTickerNews(cls, ticker):
        return cls.makeGetRequest(f"/v2/reference/news?ticker={ticker}")

    @classmethod
    def getDailyOpenClose(cls, ticker, date="2024-11-22"):
        return cls.makeGetRequest(f"/v1/open-close/{ticker}/{date}")

    @classmethod
    def getGroupedDaily(cls, date="2024-11-22"):
        # the responses are like this: 
        #   "T": (ticker)
        #   "c": (close),
        #   "h": (high),
        #   "l": (low),
        #   "n": (number of transactions),
        #   "o": (open price),
        #   "t": (timestamp for the end of the aggregate window),
        #   "v": (volume),
        #   "vw": (volume weighted average price)
        return cls.makeGetRequest(f"/v2/aggs/grouped/locale/us/market/stocks/{date}")

    @classmethod
    def getAggregate(cls, ticker, multiplier=1, timespan="hour", fromDate="2024-11-08", toDate="2024-11-23"):
        return cls.makeGetRequest(f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{fromDate}/{toDate}?limit=50000")

class Option(PolygonApi):
    # TODO: need to learn more about options to implement some of this
    pass

testOption = Option("META")
resp = testOption.getAggregate()
print(resp.json())
for bar in resp.json()["results"]:
    print(datetime.fromtimestamp(bar['t'] / 1000))