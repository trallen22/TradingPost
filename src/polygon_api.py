import time
import requests
from datetime import datetime

class PolygonApi():
    _POLYGON_API_ENDPOINT = "https://api.polygon.io"
    _POLYGON_API_KEY = "CP1nN_q8W8C4eG7phIPNgLNCyPEyDZPe" # free version 
    _TODAY_DATE_YYYY_MM_DD = datetime.today().date()
    TEST_DATE_YYYY_MM_DD = "2024-11-06" # this is just for testing

    _GOOD_RESPONSE = 200
    _API_LIMIT_RESPONSE = 429
    _SLEEP_DURATION = 10

    @classmethod
    def makeGetRequest(cls, apiEndpoint: str):
        # need to check if '?' is in apiEndpoint to allow the apiKey to be added to the end
        if ("?" not in apiEndpoint):
            apiEndpoint = f"{apiEndpoint}?"
        while True:
            response = requests.get(f"{cls._POLYGON_API_ENDPOINT}{apiEndpoint}&apiKey={cls._POLYGON_API_KEY}")
            match response.status_code:
                case cls._GOOD_RESPONSE:
                    return response.json()
                case cls._API_LIMIT_RESPONSE:
                    print(f"sleeping for {cls._SLEEP_DURATION}")
                    time.sleep(cls._SLEEP_DURATION)
                    continue
                case _:
                    raise Exception(f"got a bad response '{response.status_code}': {response.json()}")

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
    def getDailyOpenClose(cls, ticker, date=None):
        if date == None:
            date = cls._TODAY_DATE_YYYY_MM_DD
        return cls.makeGetRequest(f"/v1/open-close/{ticker}/{date}")

    @classmethod
    def getGroupedDaily(cls, date=None):
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
        if date == None:
            date = cls._TODAY_DATE_YYYY_MM_DD
        return cls.makeGetRequest(f"/v2/aggs/grouped/locale/us/market/stocks/{date}")

    @classmethod
    def getAggregate(cls, ticker, multiplier, timeIntervalType, fromDate, toDate, limit=50000):
        return cls.makeGetRequest(f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timeIntervalType}/{fromDate}/{toDate}?limit={limit}")

    @classmethod
    def getSimpleMovingAverage(cls, ticker, timestamp, timespan="day", window=50):
        return cls.makeGetRequest(f"/v1/indicators/sma/{ticker}?timestamp={timestamp}&timespan={timespan}&window={window}&expand_underlying=false")

    @classmethod
    def getRelatedCompanies(cls, ticker):
        return cls.makeGetRequest(f"/v1/related-companies/{ticker}")

    @classmethod
    def getTickerNews(cls, ticker, limit=1000):
        # TODO: need to implement published_utc
        return cls.makeGetRequest(f"/v2/reference/news?ticker={ticker}&limit={limit}")
