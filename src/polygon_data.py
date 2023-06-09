'''
This script scrapes polygon.io and returns the 50 day sma for intervals 
1 min, 5 min and 1 day as well as the 200 day sma for intervals 1 min, 5 min 
and 1 day and close price 
'''

from pkgutil import get_data
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
# TODO4: make this script format not function 
def get_indicators(tickers, dfPrint, dfParams, client, strToday):

    # use '- timedelta(1) ' to debug using yesterday's data 
    today = date.today()
    strToday = today.strftime('%Y-%m-%d')
    print(f'strToday: {strToday}')
    
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
        # TODO1: Add get_dataframe parameter values to the config file

        paramSet = [[ ticker, client, strToday, 'minute', 1, dfPrint ], 
                        [ticker, client, strToday, "minute", 5, dfPrint], 
                        [ticker, client, strToday, "day", 1, dfPrint]]

        for paramList in paramSet: 
            curDF = get_dataframe(paramList[0], paramList[1], paramList[2], paramList[3], paramList[4], paramList)

        # TODO2: break up try statement
        try:
            
            '''
            Generate 1 minute interval data
            '''
            one_minute_df = get_dataframe(ticker, client, strToday, "minute", 1, dfPrint)
            ticker_fifty_one_minute[ticker] = one_minute_df[0] # 50 interval
            ticker_two_hundred_one_minute[ticker] = one_minute_df[1] # 200 interval
            
            '''
            Generate 5 minute interval data
            '''
            five_minute_df = get_dataframe(ticker, client, strToday, "minute", 5, dfPrint)
            ticker_fifty_five_minute[ticker] = five_minute_df[0]
            ticker_two_hundred_five_minute[ticker] = five_minute_df[1]

            '''
            Generate 1 day interval data
            '''
            one_day_df = get_dataframe(ticker, client, strToday, "day", 1, dfPrint)
            ticker_fifty_one_day[ticker] = one_day_df[0]
            ticker_two_hundred_one_day[ticker] = one_day_df[1]

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

        # TODO3: make these errors on a case by case bases
        except Exception as e:
            print("Error from Polygon: " + str(e))
            ticker_fifty_one_minute[ticker] = -1
            ticker_two_hundred_one_minute[ticker] = -1
            close_dict[ticker] = -1
            ticker_fifty_five_minute[ticker] = -1
            ticker_two_hundred_five_minute[ticker] = -1
            ticker_fifty_one_day[ticker] = -1
            ticker_two_hundred_one_day[ticker] = -1

        # ensure we don't pass 5 API calls/min for polygon 
        time.sleep(30)

    return ticker_fifty_one_minute, ticker_two_hundred_one_minute, ticker_fifty_five_minute, \
    ticker_two_hundred_five_minute, ticker_fifty_one_day, ticker_two_hundred_one_day, close_dict
