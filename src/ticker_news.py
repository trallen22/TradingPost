'''
This file will manage news information. 

NOT SURE IF THIS IS NEEDED, might be able to add logic to polygon_api

log numbers 800-899
'''

import configuration_file as config
import time
from polygon.rest import models
from urllib3.exceptions import ResponseError, MaxRetryError

TEST_LIST_TICKERS = [ "AAPL", "GOOG", "AMZN", "META" ]
TEST_TICKER = "AAPL"
TEST_DATE = "2025-06-07"
NUM_RETRIES = 4
SLEEP_DURATION = 15
MAX_RESETS = 3
MAX_DEPTH = 2

class Article():
    def __init__(self, PolygonObj: models.TickerNews) -> None:
        self.title = PolygonObj.title
        self.author = PolygonObj.author
        self.article_url = PolygonObj.article_url
        self.description = PolygonObj.description

    def toDict(self):
        return {
            "title": self.title,
            "author": self.author,
            "article_url": self.article_url,
            "description": self.description
        }

    def __str__(self) -> str:
        return str(self.toDict())

def getArticlesForTicker(ticker: str, publishDate: str) -> dict:
    curArticles = dict()
    index = 0
    curTry = 0
    totalResets = 0
    newsIterable = config.CLIENT.list_ticker_news(ticker, limit=1, published_utc=publishDate)
    while curTry < NUM_RETRIES:
        success = 0
        try:
            curItem = next(iter(newsIterable))
            curArticles[f"{index}"] = Article(curItem).toDict()
            index += 1
            success = 1
            curTry = 0
        except StopIteration:
            print("finished iteration")
            break
        except ResponseError as e:
            print(f"Error 1: {e}")
        except MaxRetryError as e:
            print(f"Error 2: {e}")
        except Exception as e:
            print(f"Error 3: {e.__class__}")
        if not success:
            # reset the iterable
            newsIterable = config.CLIENT.list_ticker_news(ticker, limit=1, published_utc=publishDate)
            curArticles = dict()
            curTry += 1
            totalResets += 1
            print(f"Waiting {SLEEP_DURATION} seconds")
            time.sleep(SLEEP_DURATION)
        if totalResets == MAX_RESETS:
            print("unable to get full iterable")
            break
    if not curArticles:
        print(f"Failed to get articles for {ticker}")
    return curArticles

def getArticles(tickers: list[str]) -> dict:
    for curTicker in tickers:
        continue
    return

def getRelatedToTicker(ticker: str) -> list[str]:
    relatedTickers = []
    curRetry = 0
    while curRetry < NUM_RETRIES:
        try:
            relatedTickers = config.CLIENT.get_related_companies(ticker)
            break
        except Exception as e:
            curRetry += 1
            print(f"ERROR: failed try {curRetry} to get related tickers: {e}")
            time.sleep(SLEEP_DURATION)
    relatedTickers = map(lambda x: x.ticker, relatedTickers)
    return relatedTickers

def getAllRelatedTickers(ticker: str) -> list[str]:
    tickersToCheck = [ticker]
    alreadyChecked = set()
    depth = 0
    relatedTickers = set()
    while depth < MAX_DEPTH:
        newFinds = set()
        for t in tickersToCheck:
            if t in alreadyChecked:
                continue
            alreadyChecked.add(t)
            listCurRelated = getRelatedToTicker(t)
            newFinds.update(listCurRelated)
        depth += 1
        tickersToCheck = list(newFinds)
        relatedTickers.update(newFinds)
    return list(relatedTickers)

if __name__ == "__main__":
    for ticker in [TEST_TICKER]:
        relatedTickers = getAllRelatedTickers(ticker)
        print(relatedTickers)
        print()

