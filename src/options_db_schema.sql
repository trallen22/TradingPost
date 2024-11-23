drop schema if exists optionshistorical;
create schema optionshistorical;
use optionshistorical;

create table symbols (
    symbol_id           INT NOT NULL,
    symbol              VARCHAR(5),
    symbol_full_name    VARCHAR(100),
    primary key (symbol_id)
) ;

