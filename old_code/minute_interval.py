import yfinance as yf
import numpy as np

def get_minute_indicator(tickers):
        
    ticker_fifty_one_minute = {}    
    ticker_two_hundred_one_minute = {}

    ticker_fifty_five_minute = {}
    ticker_two_hundred_five_minute = {}

    last_price = {}

    for ticker in tickers:

        # one minute interval data 
        try: 
            df = yf.download(tickers=ticker, period='1d', interval='1m')

            last_price[ticker] = round(np.mean(df[['Close']].tail(1),axis=0).values[0],2)

            df = df[:-1]
            ## print(df.tail(50).to_string())
            # df = df[df['Volume'] > 0]
            # print(df.tail(100))
            ticker_fifty_one_minute[ticker] = round(np.mean(df[['Close']].tail(50),axis=0).values[0],2)
            # print(ticker_fifty_one_minute)
            ticker_two_hundred_one_minute[ticker] = round(np.mean(df[['Close']].tail(200),axis=0).values[0],2)
            
        except Exception as e:
            print(e)
            ticker_fifty_one_minute[ticker] = -1
            ticker_two_hundred_one_minute[ticker] = -1
            last_price[ticker] = -1

        # five minute interval data 
        try: 
            df = yf.download(tickers=ticker, period='4d', interval='5m')

            df = df[:-1]
            
            # df = df.loc[(df["Volume"] > 0)]

            ticker_fifty_five_minute[ticker] = round(np.mean(df[['Close']].tail(50),axis=0).values[0],2)
            ticker_two_hundred_five_minute[ticker] = round(np.mean(df[['Close']].tail(200),axis=0).values[0],2)

            ## print(df.tail(50).to_string())

            # print(ticker_fifty_five_minute)
            # print(ticker_two_hundred_five_minute)
        except:
            ticker_fifty_five_minute[ticker] = -1
            ticker_two_hundred_five_minute[ticker] = -1

    # return ticker_fifty_one_minute, ticker_two_hundred_one_minute, ticker_fifty_five_minute, ticker_two_hundred_five_minute, last_price

    # print(ticker_fifty_one_minute)
    # print(ticker_two_hundred_one_minute)
    # print(ticker_fifty_five_minute)
    # print(ticker_two_hundred_five_minute)
    # print(last_price)

# get_minute_indicator(["VCR"])