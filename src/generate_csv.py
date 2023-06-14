'''
This script generates a csv from scraping barchart_scrape.py
and newpoly.py
'''

import csv
import time
from polygon_data import get_indicators
import configurationFile as config

# from email_csv import send_email

def generate_csv():

    TICKERS = config.TESTTICKERS
    PARAMSET = config.PARAMSET

    with open(config.TESTCSV, mode='w') as csv_file:
        fieldnames = ['ticker', 'one_day_50',
                    'one_day_200', 'five_min_50', 
                    'five_min_200','one_min_50', 
                    'one_min_200', 'last_price']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for ticker in TICKERS:
            # uses newpoly.py
            one_minute_fifty, one_minute_two_hundred, five_minute_fifty, five_minute_two_hundred, \
        one_day_fifty, one_day_two_hundred, close_price = get_indicators(ticker, PARAMSET)
            
            writer.writerow({
                'ticker': ticker,
                'one_day_50': one_day_fifty,
                'one_day_200': one_day_two_hundred,
                'five_min_50': five_minute_fifty,
                'five_min_200': five_minute_two_hundred,
                'one_min_50': one_minute_fifty,
                'one_min_200': one_minute_two_hundred,
                'last_price': close_price
            })
            # ensure we don't pass 5 API calls/min for polygon 
            if not (ticker == TICKERS[-1]):
                time.sleep(60)

    # send_email()
