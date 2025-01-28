'''
This script scrapes polygon.io and returns the 50 day sma for intervals 
1 min, 5 min and 1 day as well as the 200 day sma for intervals 1 min, 5 min 
and 1 day and close price 

log numbers 200-299
'''

from datetime import timedelta, date
import time
import pandas as pd 
import numpy as np
from sys import exit
import configuration_file as config
from polygon_api import PolygonApi
from models import AggregateData

def convertToDataFrame(dataDict: dict) -> pd.DataFrame:
    return pd.DataFrame(dataDict)

def calculateDataBars(ticker, multiplier, timeIntervalType, fromDate, toDate):
    try:
        response = PolygonApi.getAggregate(ticker, multiplier, timeIntervalType, fromDate, toDate)
    except Exception as e:
        print(f"{e}")
    if (response["resultsCount"] == 0):
        print(f"No data was found for {ticker}")
        return {}
    barsDataPoints = AggregateData()
    for dataPoint in response['results']:
        barsDataPoints.appendDataPoint(dataPoint)
    df = pd.DataFrame(barsDataPoints.convertToDict())
    # TODO: shouldn't return the a dataframe, just return the dictionary
    # TODO: just need to use convertToDF()
    return df

# TODO: this needs to be fixed or deleted (probably deleted)
# get_indicators: gets the indices for a given ticker   
# parameters: 
#       ticker - string, etf ticker -> 'JNK'  
# returns: integers for each index. Variable names are pretty 
#           self explanatory 
def get_smas(ticker, date):
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
            while (apiLimit): # TODO: could this just be a while(True) and continue
                try:
                    curDF = get_fifty_and_200_sma(ticker, curTimeInterval, curMultiplier)
                    fifty = PolygonApi.getSimpleMovingAverage(ticker)
                    curDF = ()
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


# print(get_fifty_and_200_sma("AAPL", "day", 1))
