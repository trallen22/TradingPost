drop schema if exists tradingpost;
create schema tradingpost;
use tradingpost;
create table news (
	article_id	INT NOT NULL,
	title		VARCHAR(120), -- longest is 105
 	article_url VARCHAR(120),
	primary key (article_id)
	);