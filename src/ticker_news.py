'''
This file will manage news information. 

NOT SURE IF THIS IS NEEDED, might be able to add logic to polygon_api

log numbers 800-899
'''

import configuration_file as config
import time
from polygon.rest import models
from urllib3.exceptions import ResponseError, MaxRetryError
from database_utilities import sqlDelete, sqlInsert, sqlSelect, TEST_DATE, TICKER_NEWS_TABLE, NEWS_ARTICLES_TABLE, ARTICLE_ID_COL, ARTICLE_TITLE_COL, ARTICLE_URL_COL, ARTICLE_DESC_COL, ARTICLE_AUTHOR_COL

TEST_LIST_TICKERS = [ "AAPL", "GOOG", "AMZN", "META" ]
TEST_TICKER = "GOOGL"
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
        self.id = PolygonObj.id
        self.insertToDB()

    def insertToDB(self):
        # check if article is already in db
        article = sqlSelect(NEWS_ARTICLES_TABLE, where={ ARTICLE_ID_COL: self.id })
        if not article: # if not found, insert it in db as a sort of cache
            ret = sqlInsert(NEWS_ARTICLES_TABLE, (self.id, self.title, self.author, self.article_url, self.description, TEST_DATE))
            if ret:
                print(f"ERROR: returned {ret}")

    def toDict(self):
        return {
            "title": self.title,
            "author": self.author,
            "article_url": self.article_url,
            "description": self.description
        }

    def __str__(self) -> str:
        return str(self.toDict())

def deleteArticlesForTicker(ticker: str) -> int:
    retCode = 0
    if sqlDelete(TICKER_NEWS_TABLE, { "ticker_symbol": ticker }):
        print(f"error deleteing '{ticker}' from '{TICKER_NEWS_TABLE}'")
        retCode = 1
    return retCode

def getArticlesForTicker(ticker: str, publishDate: str) -> dict:
    curArticles = dict()
    # first check if we have the articles cached already
    joinElements = [ NEWS_ARTICLES_TABLE, f"{TICKER_NEWS_TABLE}.{ARTICLE_ID_COL}", f"{NEWS_ARTICLES_TABLE}.{ARTICLE_ID_COL}" ]
    selectElements = []
    for col in [ ARTICLE_TITLE_COL, ARTICLE_AUTHOR_COL, ARTICLE_URL_COL, ARTICLE_DESC_COL ]:
        selectElements.append(f"{NEWS_ARTICLES_TABLE}.{col}")
    dbArticles = sqlSelect(TICKER_NEWS_TABLE, select=selectElements, join=joinElements, where={ "ticker_symbol": ticker })
    # now logic depends if it's already in db
    if dbArticles:
        # index corresponds to column order in selectedElements
        for i, article in enumerate(dbArticles):
            # TODO: make this more maintainable; maybe add to Article class __init__()
            curArticles[f"{i}"] = {
                "title": article[0],
                "author": article[1],
                "article_url": article[2],
                "descripition": article[3]
            }
    else:
        index = 0
        curTry = 0
        totalResets = 0
        newsIterable = config.CLIENT.list_ticker_news(ticker, limit=1, published_utc=publishDate)
        while curTry < NUM_RETRIES:
            success = 0
            try:
                curItem = next(iter(newsIterable))
                curArticle = Article(curItem)
                curArticles[f"{index}"] = curArticle.toDict()
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
                if totalResets == MAX_RESETS:
                    print("unable to get full iterable")
                    break
                # TODO: if it fails we should delete values in the table for that ticker
                # do it down here so that we can leave some if totalResets gets hit
                # NOTE: could run the risk of only having a few of the articles
                print(f"Waiting {SLEEP_DURATION} seconds")
                time.sleep(SLEEP_DURATION)
            retCode = sqlInsert(TICKER_NEWS_TABLE, (curArticle.id, ticker, TEST_DATE))
            if retCode:
                print(f"ERROR: failed with status {retCode}")
    if not curArticles:
        print(f"Failed to get articles for {ticker}")
    return curArticles

def getRelatedToTicker(ticker: str) -> list[str]:
    RELATED_TABLE = "related_tickers"
    # first check if we already have the related tickers in the db
    relatedTickers = sqlSelect(RELATED_TABLE, where={"ticker_symbol": ticker})
    if relatedTickers: # we found something
        # eval it twice for weird sql shenanigans
        relatedTickers = eval(relatedTickers[0][1])
        relatedTickers = eval(relatedTickers) # should be a list now
    else: # no tickers returned from db
        print(f"{ticker} not found in db")
        curRetry = 0
        while curRetry < NUM_RETRIES:
            try:
                relatedTickers = config.CLIENT.get_related_companies(ticker)
                break
            except Exception as e:
                curRetry += 1
                print(f"ERROR: failed try {curRetry} to get related tickers: {e}")
                time.sleep(SLEEP_DURATION)
        relatedTickers = list(map(lambda x: x.ticker, relatedTickers))
        # we'll add the ticker to the db since we didn't have it already
        # TODO: need to implement the time
        sqlInsert(RELATED_TABLE, (ticker, f'"{relatedTickers}"', TEST_DATE))
    return relatedTickers

def getAllRelatedTickers(ticker: str, maxDepth: int=MAX_DEPTH) -> list[str]:
    tickersToCheck = [ticker]
    alreadyChecked = set()
    depth = 0
    relatedTickers = set()
    while depth < maxDepth:
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
        # relatedTickers = getAllRelatedTickers(ticker)
        # relatedTickers = getRelatedToTicker(ticker)
        # relatedTickers = getArticlesForTicker(ticker, TEST_DATE)
        relatedTickers = deleteArticlesForTicker(ticker)
        print(relatedTickers)
        print()

