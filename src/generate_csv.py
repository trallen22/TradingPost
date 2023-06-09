'''
This script generates a csv from scraping barchart_scrape.py
and newpoly.py
'''

import csv
from polygon_data import get_indicators
from datetime import date, timedelta
import configurationFile as config
# from email_csv import send_email

# TODO: Try to clean this up
to = date.today()
days = timedelta(7)
from_ = to - days
to = to.strftime('%Y-%m-%d')
from_ = from_.strftime('%Y-%m-%d')

full_time = f"{from_} to {to}"

TICKERS = config.TESTTICKERS
PRINTDF = config.PRINTDF
DFPARAM = config.DFPARAM
CLIENT = config.DFPARAM[0][0]
STRTODAY = config.STRTODAY

# TODO: Index the list
# uses newpoly.py
one_minute_fifty, one_minute_two_hundred, five_minute_fifty, five_minute_two_hundred, \
    one_day_fifty, one_day_two_hundred, close_price = get_indicators(TICKERS, PRINTDF, DFPARAM, CLIENT, STRTODAY)


with open(config.TESTCSV, mode='w') as csv_file:
    fieldnames = ['ticker', 'one_day_50',
                'one_day_200', 'five_min_50', 
                'five_min_200','one_min_50', 
                'one_min_200', 'last_price']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for ticker in TICKERS:
        writer.writerow({
            'ticker': ticker,
            'one_day_50': one_day_fifty[ticker],
            'one_day_200': one_day_two_hundred[ticker],
            'five_min_50': five_minute_fifty[ticker],
            'five_min_200': five_minute_two_hundred[ticker],
            'one_min_50': one_minute_fifty[ticker],
            'one_min_200': one_minute_two_hundred[ticker],
            'last_price': close_price[ticker]
        })

# send_email()
