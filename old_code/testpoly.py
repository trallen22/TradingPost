'''
Test file for using polygon for one_day indicator
'''
# See if can get one day averages to avoid scraping barchart 

from cmath import e
from polygon import RESTClient
from datetime import datetime, timedelta, date
# import yfinance as yf
import time
import pandas as pd 
import numpy as np


def ts_to_datetime(ts) -> str:
    return datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')

def ts_to_hour(ts) -> int:
    return int(datetime.fromtimestamp(ts / 1000.0).hour)

def ts_to_min(ts) -> int:
    return int(datetime.fromtimestamp(ts / 1000.0).minute)

def ts_to_time_of_day(ts) -> timedelta:
    return timedelta(seconds=ts.second,minutes=ts.minute,hours=ts.hour)

def get_day_indicator(tickers):
    # polygon login 
    '''Insert your key. Play around with the free tier key first.'''
    key = "nGJdIcDOy3hzWwn6X6gritFJkgDWTpRJ"
    client = RESTClient(key)

    # current day 
    # use '- timedelta(1) ' to debug using yesterday's data 
    to = datetime.today()
    days = timedelta(300)
    from_ = to - days
    to = to.strftime('%Y-%m-%d')
    from_ = from_.strftime('%Y-%m-%d')

    # dict for moving average of prices for last 50 mins of trading hours per minute
    ticker_fifty_one_day = {}

    # dict for moving average of prices for last 200 mins of trading hours per minute
    ticker_two_hundred_one_day = {}

    # Clean up new poly logic  below 
    for ticker in tickers:
        '''
        Generate 1 day interval data
        '''

        resp = client.get_aggs(ticker=ticker, multiplier=1, timespan = "day", from_=from_, to=to, adjusted=True, sort="desc")
        df = pd.DataFrame(resp)

        ######## LOOK TO OPTIMIZE AND ELIMINATE REDUNDANCY ########
        # data is given in UTC 
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, unit='ms')\
        # convert timezone from UTC to EST 
        df["timestamp"] = df["timestamp"].dt.tz_convert('US/Eastern')
        # create column that is just time of day 
        df["time_of_day"] = df["timestamp"].apply(ts_to_time_of_day)

        # use time of day to filter normal market hours 

        # probably don't need this line
        # market_open = timedelta(seconds=0, minutes=30, hours=9) 

        market_close = timedelta(seconds=0, minutes=59, hours=15)
        df = df[df["time_of_day"] <= market_close]

        # assigns value of ticker to simple moving average of last 50mins of before market close and rounds to two decimal
        ticker_fifty_one_day[ticker] = round(np.mean(df[["close"]].head(50),axis=0).values[0],2)

        # assigns value of ticker to simple moving average of last 200mins of before market close and rounds to two decimal
        ticker_two_hundred_one_day[ticker] = round(np.mean(df[["close"]].head(200)).values[0],2)

        print('--- 1 day ---')
        print(df)
        print('------')

    return ticker_fifty_one_day, ticker_two_hundred_one_day 

