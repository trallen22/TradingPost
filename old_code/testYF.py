import yfinance as yf
import numpy as np
import pandas as pd
from datetime import date

ticker = "VIG"

# tickers -> list of tickers 
# period -> time period 
# interval -> trading interval 
df = yf.download(tickers=ticker, period='2d', interval='1m')



# sets dataframe index back to zero 
df.reset_index(level=0, inplace=True)
# sets the Datetime column as a string
df["Datetime"] = df["Datetime"].astype(str)

# adds a "Day" column using the "Datetime" string 
df["Day"] = df["Datetime"].str[:10]
df["Datetime"] = pd.to_datetime(df["Datetime"])
df["Day"] = pd.to_datetime(df["Day"])

# gets the information for today
desired = pd.to_datetime(date.today())

# gets the information for day before today 
df = df.loc[df['Day'] < desired]


# gets mean of last 50 opens and rounds to 2 decimal places 
ticker_fifty_one_minute = round(np.mean(df[['Open']].tail(50)).values[0],2)
print(ticker_fifty_one_minute)

# gets mean of last 200 opens and rounds to 2 decimal places 
ticker_two_hundred_one_minute = round(np.mean(df[['Open']].tail(200)).values[0],2)


# # print(df.columns)

last_price = round(np.mean(df[['Open']].tail(1)).values[0],2)
print(last_price)

print(df[["Datetime","Open","Close","Adj Close"]].tail())
