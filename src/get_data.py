'''
This script scrapes polygon.io and returns the 50 day sma for intervals 
1 min, 5 min and 1 day as well as the 200 day sma for intervals 1 min, 5 min 
and 1 day and close price 

log numbers 200-299
'''

from datetime import timedelta
import time
import pandas as pd 
import numpy as np
from sys import exit

import configuration_file as config

# I didn't create this function and I honestly don't know what it means 
def ts_to_time_of_day(ts) -> timedelta:
    return timedelta(seconds=ts.second,minutes=ts.minute,hours=ts.hour)

# get_dataframe: helper function for get_indicators(). Gets the 50 and 
#                   200 values for a given index. (ex: 1 min, 5 min, 1 day) 
# parameters: 
#       curTicker - string, etf ticker -> 'JNK' 
#       timeUnit - string, time interval (minute, day) 
#       intMultiplier - integer, interval multiplier (1, 5) 
# returns: returns the 50 and 200 sma values for a given ticker and time interval 
def get_dataframe(curTicker, timeUnit, intMultiplier):

    config.logmsg('DEBUG', 200, f"Retrieving data for {curTicker} - {intMultiplier} {timeUnit}")

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

    # in case the market closes early and values get skewed
    df = df[df["transactions"].notnull()]

    # assigns value of ticker to simple moving average of last 50mins of before market close and rounds to two decimal
    fifty_interval = round(np.mean(df[["close"]].head(50),axis=0).values[0],2)

    # assigns value of ticker to simple moving average of last 200mins of before market close and rounds to two decimal
    two_hundred_interval = round(np.mean(df[["close"]].head(200), axis=0).values[0],2)

    # prints each dataframe. Used for debugging 
    if (config.PRINTDF):
        print('#################')
        print(f'--- {intMultiplier} {timeUnit} ---')
        print('#################')
        print(df)
    config.logmsg('DEBUG', 201, f"Data retrieved for {curTicker} - {intMultiplier} {timeUnit}")
    return fifty_interval, two_hundred_interval

# get_indicators: gets the indices for a given ticker   
# parameters: 
#       ticker - string, etf ticker -> 'JNK'  
# returns: integers for each index. Variable names are pretty 
#           self explanatory 
def get_indicators(ticker):
    finalIndexes = []
    config.logmsg('DEBUG', 203, f'Starting indicator retrieval for ticker \'{ticker}\'')
    # Generate 50 and 200 for given time interval(s) in paramSet
    for i in range(len(config.PARAMSET)):

        config.logmsg('DEBUG', 204, f'Processing iteration {i + 1}/{len(config.PARAMSET)}')
        curTimeInterval = config.PARAMSET[i][0] # time interval (minute, day) 
        curMultiplier = config.PARAMSET[i][1] # multiplier for time interval 

        apiLimit = 1 # need this for free version 
        downTime = 0
        try: 
            # Loop while unable to get api call 
            while (apiLimit):
                try:
                    curDF = get_dataframe(ticker, curTimeInterval, curMultiplier)
                    apiLimit = 0
                    downTime = 0
                except Exception:
                    time.sleep(5)
                    if (config.DEBUG):
                        if (not downTime % 10):
                            config.logmsg('DEBUG', 200 + 2 * i, f'api call failed for {downTime} seconds')
                        downTime += 5
                        if (downTime > 80):
                            config.logmsg('ERROR', 201 + 2 * i, f'failed to call api for {downTime} seconds')
                            exit(1)
            finalIndexes.append(curDF[0])
            finalIndexes.append(curDF[1])
        except Exception as e:
            config.logmsg('ERROR', 220, f'{e}')
            config.logmsg('NOTICE', 221, f'problem getting indicator {config.PARAMSET[i]} for ticker \'{ticker}\'')
            config.logmsg('DEBUG', 243, f'indicator {config.PARAMSET[i]} set to -1 for \'{ticker}\'')
            finalIndexes.append(-1)
            finalIndexes.append(-1) 

    ticker_fifty_one_minute = finalIndexes[0]
    ticker_two_hundred_one_minute = finalIndexes[1]
    ticker_fifty_five_minute = finalIndexes[2]
    ticker_two_hundred_five_minute = finalIndexes[3]
    ticker_fifty_one_day = finalIndexes[4]
    ticker_two_hundred_one_day = finalIndexes[5]
    
    # generate closing price 
    try: 
        close_price = config.CLIENT.get_daily_open_close_agg(ticker=ticker, date=str(config.today)).close
        config.logmsg('DEBUG', 205, f'Successfully retrieved close price for \'{ticker}\': {close_price}')
    except Exception as e:
        config.logmsg('ERROR', 239, f'{e}')
        config.logmsg('NOTICE', 241, f"make sure it isn\'t a weekend")
        config.logmsg('NOTICE', 240, f'problem getting close price for \'{ticker}\' on \'{config.today}\'')
        close_price = -1
        config.logmsg('DEBUG', 242, f'close price set to -1 for \'{ticker}\'')

    config.logmsg('DEBUG', 206, f'Indicator retrieval completed for ticker \'{ticker}\'')
    return ticker_fifty_one_minute, ticker_two_hundred_one_minute, ticker_fifty_five_minute, \
    ticker_two_hundred_five_minute, ticker_fifty_one_day, ticker_two_hundred_one_day, close_price
