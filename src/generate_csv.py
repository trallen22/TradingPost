'''
This script generates a csv from scraping barchart_scrape.py
and newpoly.py
'''

import csv
import configurationFile as config

# from email_csv import send_email

def generate_csv(etf, mode):
    etfVals = etf.indicatorDict
    fieldnames = ['ticker', 'one_day_50',
                'one_day_200', 'five_min_50', 
                'five_min_200','one_min_50', 
                'one_min_200', 'last_price']
    if (mode == 'w'):
        with open(config.CSVFILE, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'ticker': etf.ticker,
                'one_day_50': etfVals['one_day_50'],
                'one_day_200': etfVals['one_day_200'],
                'five_min_50': etfVals['five_min_50'],
                'five_min_200': etfVals['five_min_200'],
                'one_min_50': etfVals['one_min_50'],
                'one_min_200': etfVals['one_min_200'],
                'close_price': etfVals['close_price']
            })
    else:
        with open(config.CSVFILE, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({
                'ticker': etf.ticker,
                'one_day_50': etfVals['one_day_50'],
                'one_day_200': etfVals['one_day_200'],
                'five_min_50': etfVals['five_min_50'],
                'five_min_200': etfVals['five_min_200'],
                'one_min_50': etfVals['one_min_50'],
                'one_min_200': etfVals['one_min_200'],
                'last_price': etfVals['close_price']
            })

    # send_email()
