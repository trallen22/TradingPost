'''
This file will manage news information. 

NOT SURE IF THIS IS NEEDED, might be able to add logic to polygon_api

log numbers 800-899
'''

from polygon_api import PolygonApi
import configuration_file as config
import json

TEST_LIST_TICKERS = [ "AAPL", "GOOG", "AMZN", "META" ]
TEST_TICKER = "AAPL"
TEST_RESP_LIMIT = 1

class Article():
    def __init__(self, article_api=None, publisher_name=None, title=None, description=None, article_url=None):
        # TODO: should try to implement sentiment somehow
        self.publisher_name = article_api['publisher']['name']
        self.title = article_api['title']
        self.article_url = article_api['article_url']
        self.associated_tickers = article_api['tickers']

    def __eq__(self, other):
        if isinstance(other, Article):
            return self.article_url == other.article_url
        return False

    def __hash__(self):
        return hash(self.article_url)

class TickerNews():
    def __init__(self) -> None:
        self.articles = []
        self.articlesWithWeights = {} # { Article: <num instances>, ... }
        self.dictTickerArticles = {} # this would hold ticker and related articles; psuedo caching
        self.tickers = set()

    def WeightNewsHighestVolumeArticles(self) -> dict[Article: int]:
        self.articlesWithWeights = {}
        for i in self.articles:
            try:
                self.articlesWithWeights[i] += 1
            except:
                self.articlesWithWeights[i] = 1

    def returnNewsHighestVolumeArticles(self, numArticles=None):
        listArticles = sorted(self.articlesWithWeights, key=self.articlesWithWeights.get, reverse=True)
        if (isinstance(numArticles, int) and numArticles > 0):
            listArticles = listArticles[:numArticles]
        return listArticles

    def callNewsApi(self, ticker=None, published_utc=None, order=None, limit=1000, sort=None):
        tickerParam = f"ticker={ticker}"
        limitParam = f"&limit={limit}"
        newsData = PolygonApi.makeGetRequest(f"/v2/reference/news?{tickerParam}{limitParam}")
        for i in newsData["results"]:
            curArticle = Article(i)
            self.articles.append(curArticle)
            try:
                self.dictTickerArticles[ticker].append(curArticle)
            except:
                self.dictTickerArticles[ticker] = [curArticle]

    def getArticlesForTicker(self, ticker=None):
        if (not ticker in self.tickers):
            config.logmsg("DEBUG", 800, f"calling api for article for ticker '{ticker}'")
            self.callNewsApi(ticker)
        return self.dictTickerArticles[ticker]
        

    def __str__(self):
        return json.dumps(self.dictTickerArticles, indent=4)

if __name__ == "__main__":
    testArticles = []
    testNews = TickerNews()
    for ticker in TEST_LIST_TICKERS:
        testArticles.append(testNews.getArticlesForTicker(ticker))
    testNews.WeightNewsHighestVolumeArticles()
    relativeArticles = testNews.returnNewsHighestVolumeArticles(numArticles=5)
    for i in relativeArticles:
        print(i.title)
        print(i.article_url)
        print()
