'''
This file will manage news information. 

NOT SURE IF THIS IS NEEDED, might be able to add logic to polygon_api

log numbers 800-899
'''

import configuration_file as config
from polygon.rest import models

TEST_LIST_TICKERS = [ "AAPL", "GOOG", "AMZN", "META" ]
TEST_TICKER = "AAPL"
TEST_DATE = "2025-05-20"

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
    for i in config.CLIENT.list_ticker_news(ticker, limit=1000, published_utc=publishDate):
        curArticles[f"{index}"] = Article(i).toDict()
        index += 1
    return curArticles

def getArticles(tickers: list[str]) -> dict:
    for curTicker in tickers:
        continue
    return

if __name__ == "__main__":
    for ticker in TEST_LIST_TICKERS:
        testArts = getArticlesForTicker(ticker, TEST_DATE)
        for i in range(len(testArts)):
            print(testArts[f"{i}"])
            print(type(i))
            print()
        break
