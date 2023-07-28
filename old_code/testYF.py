import yfinance as yf
import numpy as np
import pandas as pd
from datetime import date, datetime, time
import configuration_file as config

print(config.today)

for ticker in config.TICKERS:
    etf = yf.Ticker(ticker)
    info = etf.history()
    print(round(info['Close'][f'{config.today} 00:00:00-04:00'], 2))

    for i in etf.info:
        print(i)
    print(round(etf.info['fiftyDayAverage'], 2))
    print(round(etf.info['twoHundredDayAverage'], 2))
