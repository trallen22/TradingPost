
from polygon import RESTClient
from datetime import datetime, timedelta
# import yfinance as yf
import time
import pandas as pd 
import numpy as np
import pytz


# pd.set_option("display.max_rows", None, "display.max_columns", None)

def ts_to_datetime(ts) -> str:
    return datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')

def ts_to_hour(ts) -> int:
    return int(datetime.fromtimestamp(ts / 1000.0).hour)

def ts_to_min(ts) -> int:
    return int(datetime.fromtimestamp(ts / 1000.0).minute)

def ts_to_time_of_day(ts) -> timedelta:
    return timedelta(seconds=ts.second,minutes=ts.minute,hours=ts.hour)

def get_minute_indicator(tickers):

    # polygon login 
    '''Insert your key. Play around with the free tier key first.'''
    key = "nGJdIcDOy3hzWwn6X6gritFJkgDWTpRJ"
    client = RESTClient(key)

    # current day 
    # use '- timedelta(1) ' to debug using yesterday's data 
    to = datetime.today()
    days = timedelta(7)
    from_ = to - days

    to = to.strftime('%Y-%m-%d')

    print(to)
    from_ = from_.strftime('%Y-%m-%d')
        
    ticker_fifty_one_minute = {}  
    print(ticker_fifty_one_minute)  
    ticker_two_hundred_one_minute = {}

    ticker_fifty_five_minute = {}
    ticker_two_hundred_five_minute = {}

    # last_price = {}

    for ticker in tickers:

        try:


            '''
            Generate 1 minute interval data
            '''
            resp = client.get_aggs(ticker=ticker, multiplier=1, timespan = "minute", from_=from_, to=to, adjusted=True, sort="desc")
            df = pd.DataFrame(resp)
            
            # data is given in UTC 
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, unit='ms')\
            # convert timezone from UTC to EST 
            df["timestamp"] = df["timestamp"].dt.tz_convert('US/Eastern')
            # create column that is just time of day 
            df["time_of_day"] = df["timestamp"].apply(ts_to_time_of_day) 

            # use time of day to filter normal market hours 
            market_open = timedelta(seconds=0, minutes=30, hours=9)
            market_close = timedelta(seconds=0, minutes=59, hours=15)
            df = df[(df["time_of_day"] >= market_open) & (df["time_of_day"] <= market_close)]

            # use for debugging 
            # print(df.head(100).to_string())

            ticker_fifty_one_minute[ticker] = round(np.mean(df[["close"]].head(50)).values[0],2)
            ticker_two_hundred_one_minute[ticker] = round(np.mean(df[["close"]].head(200)).values[0],2)
            
            '''
            Generate 5 minute interval data
            '''
            resp = client.get_aggs(ticker=ticker, multiplier=5, timespan = "minute", from_=from_, to=to, adjusted=True, sort="desc")
            df = pd.DataFrame(resp)

            # data is given in UTC 
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, unit='ms')\
            # convert timezone from UTC to EST 
            df["timestamp"] = df["timestamp"].dt.tz_convert('US/Eastern')
            # create column that is just time of day 
            df["time_of_day"] = df["timestamp"].apply(ts_to_time_of_day) 

            # use time of day to filter normal market hours 
            market_open = timedelta(seconds=0, minutes=30, hours=9)
            market_close = timedelta(seconds=0, minutes=59, hours=15)
            df = df[(df["time_of_day"] >= market_open) & (df["time_of_day"] <= market_close)]

            # print(df.head(200).to_string())

            ticker_fifty_five_minute[ticker] = round(np.mean(df[["close"]].head(50)).values[0],2)
            ticker_two_hundred_five_minute[ticker] = round(np.mean(df[["close"]].head(200)).values[0],2)

            '''
            Generate closing price data
            '''
            # resp = client.get_aggs(ticker=ticker, multiplier=1, timespan = "day", from_=to, to=to, adjusted=True, sort="desc")
            # df = pd.DataFrame(resp)
            # df["timestamp"] = df["timestamp"].apply(ts_to_datetime)
            # last_price[ticker] = df.at[0,'close']



            '''
            testing to not scrape for daily interval
            # from_ = datetime.today() - timedelta(days=500)
            # from_ = from_.strftime('%Y-%m-%d')
            # resp = client.get_aggs(ticker=ticker, multiplier=1, timespan = "day", from_=from_, to=to, adjusted=True, sort="desc")
            # df = pd.DataFrame(resp)

            # # data is given in UTC 
            # df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, unit='ms')\
            # # convert timezone from UTC to EST 
            # df["timestamp"] = df["timestamp"].dt.tz_convert('US/Eastern')

            # print(df.head(10).to_string())
            '''
            # break

            # df["hour"] = df["timestamp"].apply(ts_to_hour)  
            # df["minute"] = df["timestamp"].apply(ts_to_min)  
            # df["minutes_since_midnight"] = df["hour"]*60 + df["minute"]
            # df["min_mod_5"] = df["minute"] % 5
            # df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms', utc=True)
            # df["timestamp"] = df["timestamp"].dt.tz_localize('UTC')
            # .apply(ts_to_datetime)

            '''
            Test for normal market hours
            print("TIME TEST")
            today = datetime.today()
            time_test = datetime(today.year,today.month,today.day) + timedelta(seconds=0, minutes=59, hours=15)
            # datetime(today.year, today.month, 1)
            print(time_test)
            print(type(time_test))
            print()
            print(df.timestamp.dtype)
            df = df[(df['timestamp'] <= time_test)]

            # df["time_of_day"] = df['timestamp'].apply(lambda x: timedelta(x['timestamp'].second,x['timestamp'].minute,x['timestamp'].hour))
            df["time_of_day"] = df["timestamp"].apply(ts_to_time_of_day) 

            market_open = timedelta(seconds=0, minutes=30, hours=9)
            market_close = timedelta(seconds=0, minutes=59, hours=15)
            df = df[(df["time_of_day"] >= market_open) & (df["time_of_day"] <= market_close)]

            # df = df[df.apply(lambda x: x['timestamp'].hour < 16, axis=1)]
            # df = df[df.apply(lambda x: x['timestamp'].hour > 9, axis=1)]
            '''

            # print(df.dtypes)
            
            # close_time = to + " 15:59" 

            # close_time = to + " 15:10" 

            # only want times where trades occured and until 3:59 close 
            # df = df.loc[(df["transactions"] > 0)]
            # df = df.loc[(df["timestamp"] <= close_time)]     

            # polygon does not seem to include when transactions == 0 
            # df = df.loc[(df["transactions"] == 0)]

            # reverse order, most recent on top 
            # df = df.iloc[::-1]

            # print(df.head(100).to_string())

            # # one minute interval and last price data 
            # ticker_fifty_one_minute[ticker] = round(np.mean(df[["close"]].head(50)).values[0],2)
            # ticker_two_hundred_one_minute[ticker] = round(np.mean(df[["close"]].head(200)).values[0],2)

            # resp = client.get_daily_open_close_agg(ticker=ticker, date = to, adjusted=True)

            # print(resp)
            # df = pd.DataFrame(resp)

            # print(df)

            # try:
            #     df = yf.download(tickers=ticker, period='1d', interval='1m')
            #     last_price[ticker] = round(np.mean(df[['Close']].tail(1),axis=0).values[0],2)

            # except Exception as e:
            #     print("Yahoo Finance Error: " + str(e))

            # print(ticker_fifty_one_minute)
            # print(ticker_two_hundred_one_minute)

            # five minute interval data 
            # verify this 15:55 is what to use 
            # df = df.loc[(df["timestamp"] <= to + " 15:55")]

            # df = df.loc[(df["minute"] % 5 == 4)]

            # resp = client.get_aggs(ticker=ticker, multiplier=5, timespan = "minute", from_=from_, to=to, adjusted=True, sort="desc")
            # df = pd.DataFrame(resp)

            # # 959 corresponds to 15:59 
            # df = df.loc[(df["minutes_since_midnight"] <= 959)]
            # # 570 corresponds to 09:30 
            # df = df.loc[(df["minutes_since_midnight"] >= 570)]   

            # # print(df.head(200).to_string())
            # df = df.iloc[::5, :]

            # print(df.head(200).to_string())

            # ticker_fifty_five_minute[ticker] = round(np.mean(df[["close"]].head(50)).values[0],2)
            # ticker_two_hundred_five_minute[ticker] = round(np.mean(df[["close"]].head(200)).values[0],2)

            # print(df.to_string())

            # print(ticker_fifty_five_minute)
            # print(ticker_two_hundred_five_minute)
            # print(last_price)

            # resp = client.get_aggs(ticker=ticker, multiplier=1, timespan = "day", from_=to, to=to, adjusted=True, sort="desc")
            # df = pd.DataFrame(resp)
            # df["timestamp"] = df["timestamp"].apply(ts_to_datetime)
            # last_price[ticker] = df.at[0,'close']
            # print("Daily interval")
            # print(df.at[0,'close'])
            
            # print(df)   

        # could not get polygon data 
        except Exception as e:
            print("Error from Polygon: " + str(e))
            ticker_fifty_one_minute[ticker] = -1
            ticker_two_hundred_one_minute[ticker] = -1
            # last_price[ticker] = -1
            ticker_fifty_five_minute[ticker] = -1
            ticker_two_hundred_five_minute[ticker] = -1

        # ensure we don't pass 5 API calls/min for polygon 
        time.sleep(60)

    # print(ticker)
    # print(ticker_fifty_one_minute)
    # print(ticker_two_hundred_one_minute)
    # print(ticker_fifty_five_minute)
    # print(ticker_two_hundred_five_minute)
    # print(last_price)
    # print()

    return ticker_fifty_one_minute, ticker_two_hundred_one_minute, ticker_fifty_five_minute, ticker_two_hundred_five_minute
    # return ticker_fifty_one_minute, ticker_two_hundred_one_minute, ticker_fifty_five_minute, ticker_two_hundred_five_minute, last_price
    # print(ticker_fifty_one_minute)
    # print(ticker_two_hundred_one_minute)
    # print(ticker_fifty_five_minute)
    # print(ticker_two_hundred_five_minute)
    # print(last_price)

# get_minute_indicator('VOO')
