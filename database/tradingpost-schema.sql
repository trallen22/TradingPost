-- drop table if exists related_tickers;
drop table if exists ticker_news;
drop table if exists news_articles;

-- create table related_tickers (
-- 	ticker_symbol	VARCHAR, -- for now VARCHAR is probably fine
-- 	related_tickers	VARCHAR, -- this'll be a list of tickers
-- 	last_update		DATE, -- this'll be used to see if we need to update any tickers
-- 	primary key (ticker_symbol)
-- );

-- news_articles holds the information for the individual articles
create table news_articles (
	article_id		VARCHAR NOT NULL,
	article_title	VARCHAR,
	article_author	VARCHAR,
	article_url		VARCHAR,
	article_desc	VARCHAR,
	last_update		DATE,
	primary key (article_id)
);

-- ticker_news holds an article and the tickers it was found from
create table ticker_news (
	article_id		VARCHAR NOT NULL,
	ticker_symbol	VARCHAR NOT NULL,
	last_update		DATE,
	primary key (article_id, ticker_symbol),
	foreign key (article_id) references news_articles(article_id)
);
