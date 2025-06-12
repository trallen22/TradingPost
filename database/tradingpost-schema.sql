drop table if exists related_tickers;

create table related_tickers (
	ticker_symbol	VARCHAR, -- for now VARCHAR is probably fine
	related_tickers	VARCHAR, -- this'll be a list of tickers
	last_update		DATE, -- this'll be used to see if we need to update any tickers
	primary key (ticker_symbol)
);

-- create table news (
-- 	article_id	INT NOT NULL,
-- 	title		VARCHAR(120), -- longest is 105
--  	article_url VARCHAR(120),
-- 	primary key (article_id)
-- 	);