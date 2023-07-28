'''
This script scrapes polygon.io and returns the 50 day sma for intervals 
1 min, 5 min and 1 day as well as the 200 day sma for intervals 1 min, 5 min 
and 1 day and close price 
'''

from datetime import timedelta
import time
import pandas as pd 
import numpy as np
import yfinance as yf
from sys import exit

import configuration_file as config

def ts_to_time_of_day(ts) -> timedelta:
    return timedelta(seconds=ts.second,minutes=ts.minute,hours=ts.hour)

'''
get_dataframe - Called by get_indicators(), Gets the dataframe for the given ticker and time interval 
'''
def get_dataframe(curTicker, timeUnit, intMultiplier):

    endDay = config.today

    if timeUnit == 'minute':
        days = timedelta(7)
    elif timeUnit == 'day':
        days = timedelta(300)
    else: 
        print('Invalid time unit')
        exit(5)

    startDay = endDay - days
    startDay = startDay.strftime('%Y-%m-%d')

    # call to polygon.io api 
    resp = config.CLIENT.get_aggs(ticker=curTicker, multiplier=intMultiplier, timespan = timeUnit, from_=startDay, to=config.STRTODAY, adjusted=True, sort="desc")
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

    df = df[df["transactions"].notnull()]

    # assigns value of ticker to simple moving average of last 50mins of before market close and rounds to two decimal
    fifty_interval = round(np.mean(df[["close"]].head(50),axis=0).values[0],2)

    # assigns value of ticker to simple moving average of last 200mins of before market close and rounds to two decimal
    two_hundred_interval = round(np.mean(df[["close"]].head(200)).values[0],2)

    # prints each dataframe. Used for debugging 
    if (config.PRINTDF):
        print('#################')
        print(f'--- {intMultiplier} {timeUnit} ---')
        print('#################')
        print(df)

    return fifty_interval, two_hundred_interval

'''
Gets the sma values for each ticker
'''
def get_indicators(ticker):

    finalIndexes = []

    '''
    Generate 50 and 200 for given time interval(s) in paramSet
    '''
    for i in range(len(config.PARAMSET)): 

        curTimeInterval = config.PARAMSET[i][0] # time interval (minute, day) 
        curMultiplier = config.PARAMSET[i][1] # multiplier for time interval 

        apiLimit = 1
        downTime = 0
        try: 
            # Loop while too many api calls per minute
            while (apiLimit):
                try:
                    curDF = get_dataframe(ticker, curTimeInterval, curMultiplier)
                    apiLimit = 0
                    downTime = 0
                except Exception:
                    time.sleep(5)
                    if (config.DEBUGDATA or config.DEBUG):
                        if (not downTime % 10):
                            print(f'DEBUG:{ticker}: api call failed for {downTime} seconds')
                        downTime += 5
                        if (downTime > 70):
                            print(f'ERROR:{ticker} get_data failed after {downTime} seconds')
                            exit(9)
            finalIndexes.append(curDF[0])
            finalIndexes.append(curDF[1])
        except Exception as e:
            print(f'ERROR: {e}')
            print(f'NOTICE: problem getting indicator {i} for ticker \"{ticker}\"')
            finalIndexes.append(-1)
            finalIndexes.append(-1) 

    ticker_fifty_one_minute = finalIndexes[0]
    ticker_two_hundred_one_minute = finalIndexes[1]
    ticker_fifty_five_minute = finalIndexes[2]
    ticker_two_hundred_five_minute = finalIndexes[3]
    ticker_fifty_one_day = finalIndexes[4]
    ticker_two_hundred_one_day = finalIndexes[5]

    '''
    Generate closing price by date 
    '''
    try: 
        # you just gotta look up how this works 
        etf = yf.Ticker(ticker)
        info = etf.history()
        close_price = round(info['Close'][f'{config.today} 00:00:00-04:00'], 2)
    except KeyError as keyErr:
        print(f'ERROR in get_indicators(): {keyErr}')
        exit(3)

    return ticker_fifty_one_minute, ticker_two_hundred_one_minute, ticker_fifty_five_minute, \
    ticker_two_hundred_five_minute, ticker_fifty_one_day, ticker_two_hundred_one_day, close_price
