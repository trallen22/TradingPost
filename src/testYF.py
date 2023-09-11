import yfinance as yf
import numpy as np
import pandas as pd
from datetime import date, datetime, time
import configuration_file as config
import csv

# print(config.today)

TICKERS = [ 'JNK', 'GDX', 'VCR', 'VDC', 'VIG', 'VDE', 'VFH', 
    'VWO', 'VHT', 'VIS', 'VGT', 'VAW', 'VNQ', 'VOO', 
    'VOX', 'BND', 'BNDX', 'VXUS', 'VTI', 'VPU', 'XTN' ]

TICKERS = [ 'JNK' ]

file = '/Users/tristanallen/Desktop/TradingPost/testTP/09-01_csv.csv'

# with open(file, mode='r') as curFile:
#     # curCsv = csv.reader(curFile)
#     curCsv = csv.DictReader(curFile)
    
#     for line in curCsv:
#         print(line)

#     # for line in curCsv:
#     #     print(line)

for ticker in TICKERS:
    print(ticker)
    etf = yf.Ticker(ticker)
    info = etf.history(start="2023-01-01", end=config.STRTOMORROW, interval="1d")
    # print(round(info['Close'][f'{config.today} 00:00:00-04:00'], 2))
    # print("INFO")
    # print(info.tail(50)) # getting last few rows 
    # info['Close'] = round(info['Close'], 2)
    # print(info.tail(50))
    # fifty_interval = round(np.mean(info["Close"].tail(50),axis=0),2)
    # print(f"test 50 day sma: {fifty_interval}")
    # print('--------')
    print("INFO")
    print(etf.info['previousClose'])
    print(f"50 day sma: {round(etf.info['fiftyDayAverage'], 2)}")
    print(f"200 day sma: {round(etf.info['twoHundredDayAverage'], 2)}")
    print("--------")
