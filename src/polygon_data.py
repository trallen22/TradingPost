'''
This script scrapes polygon.io and returns the 50 day sma for intervals 
1 min, 5 min and 1 day as well as the 200 day sma for intervals 1 min, 5 min 
and 1 day and close price 
'''

from pkgutil import get_data
from typing import final
from polygon import RESTClient
from datetime import datetime, timedelta, date
import time
import pandas as pd 
import numpy as np
import configurationFile as config

def ts_to_datetime(ts) -> str:
    return datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')

def ts_to_hour(ts) -> int:
    return int(datetime.fromtimestamp(ts / 1000.0).hour)

def ts_to_min(ts) -> int:
    return int(datetime.fromtimestamp(ts / 1000.0).minute)

def ts_to_time_of_day(ts) -> timedelta:
    return timedelta(seconds=ts.second,minutes=ts.minute,hours=ts.hour)

'''
get_dataframe - Called by get_indicators(), Gets the dataframe for the given ticker and time interval 
'''
def get_dataframe(curTicker, client, strToday, timeUnit, intMultiplier, printDF=0):
    # TODO7: in get_dataframe Fix time delta for one day interval -> timedelta(300)
    to = date.today()
    days = timedelta(7)
    ffrom_ = to - days
    ffrom_ = ffrom_.strftime('%Y-%m-%d')

    # call to polygon.io api 
    resp = client.get_aggs(ticker=curTicker, multiplier=intMultiplier, timespan = timeUnit, from_=ffrom_, to=strToday, adjusted=True, sort="desc")
    df = pd.DataFrame(resp)

    # converts UTC timestampt to EST and creates time of day column
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, unit='ms')
    df["timestamp"] = df["timestamp"].dt.tz_convert('US/Eastern')
    df["time_of_day"] = df["timestamp"].apply(ts_to_time_of_day)

    # use time of day to filter normal market hours 
    market_open = timedelta(seconds=0, minutes=30, hours=9)
    market_close = timedelta(seconds=0, minutes=59, hours=15)

    df = df[df["time_of_day"] <= market_close]
    if (timeUnit == 'minute'):
        df = df[df["time_of_day"] >= market_open]
    
    # assigns value of ticker to simple moving average of last 50mins of before market close and rounds to two decimal
    fifty_interval = round(np.mean(df[["close"]].head(50),axis=0).values[0],2)

    # assigns value of ticker to simple moving average of last 200mins of before market close and rounds to two decimal
    two_hundred_interval = round(np.mean(df[["close"]].head(200)).values[0],2)

    if (printDF):
        print(f'--- {intMultiplier} {timeUnit} ---')
        print(df)
        print('--------')

    return fifty_interval, two_hundred_interval

'''
Gets the sma values for each ticker
'''
# TODO4: make get_indicators script format not function 
def get_indicators(tickers, dfPrint, dfParams, client, strToday, paramSet):

    # use '- timedelta(1) ' to debug using yesterday's data 
    today = date.today()
    strToday = today.strftime('%Y-%m-%d')
    
    minDelta = timedelta(7)
    minDays = today - minDelta

    daysDelta = timedelta(300)
    daysDays = today - daysDelta

    ticker_fifty_one_minute = {} # dict 50 sma 1 min interval
    ticker_two_hundred_one_minute = {} # dict 200 sma 1 min interval
    ticker_fifty_five_minute = {} # dict 50 sma 5 min interval
    ticker_two_hundred_five_minute = {} # dict 200 sma 5 min interval
    ticker_fifty_one_day = {} # dict 50 sma 1 day interval
    ticker_two_hundred_one_day = {} # dict 200 sma 1 day interval
    close_dict = {} # dict of closing prices

    for ticker in tickers:
        finalIndexes = []

        '''
        Generate 50 and 200 for given time interval 
        '''
        for i in range(len(paramSet)): 
            # curTicker = paramSet[i][0] # need to remove 
            curClient = paramSet[i][1]
            curStrToday = paramSet[i][2]
            curTimeInterval = paramSet[i][3]
            curMultiplier = paramSet[i][4]
            curdfPrint = paramSet[i][5]
            try: 
                curDF = get_dataframe(ticker, curClient, curStrToday, curTimeInterval, curMultiplier, curdfPrint)
                finalIndexes.append(curDF[0])
                finalIndexes.append(curDF[1])
            except Exception as e:
                finalIndexes.append(-1)
                finalIndexes.append(-1) 

        ticker_fifty_one_minute[ticker] = finalIndexes[0]
        ticker_two_hundred_one_minute[ticker] = finalIndexes[1]
        ticker_fifty_five_minute[ticker] = finalIndexes[2]
        ticker_two_hundred_five_minute[ticker] = finalIndexes[3]
        ticker_fifty_one_day[ticker] = finalIndexes[4]
        ticker_two_hundred_one_day[ticker] = finalIndexes[5]

        '''
        Generate closing price by date 
        '''
        try:
            # this needs to be run after midnight 
            close_price = client.get_daily_open_close_agg(ticker=ticker, date=str(date.today() - timedelta(1))).close
            close_dict[ticker] =  close_price if not close_price == '' else -1
        except Exception as f:
            print(f)
            close_dict[ticker] = -1

        # ensure we don't pass 5 API calls/min for polygon 
        time.sleep(30)


    return ticker_fifty_one_minute, ticker_two_hundred_one_minute, ticker_fifty_five_minute, \
    ticker_two_hundred_five_minute, ticker_fifty_one_day, ticker_two_hundred_one_day, close_dict
