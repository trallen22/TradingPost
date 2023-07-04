'''
This script generates a csv from a dictionary of etf objects
'''

import csv
import configurationFile as config

# generate_csv: generates a csv file with path config.CSVFILE
# parameters: 
#       etfDict - a dictionary of etf objects 
# returns: no return value. generates a csv file to given path
def generate_csv(etfDict):
    with open(config.CSVFILE, mode='w') as csv_file:
        fieldnames = ['ticker', 'one_day_50',
                        'one_day_200', 'five_min_50', 
                        'five_min_200','one_min_50', 
                        'one_min_200', 'close_price']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for ticker in config.TICKERS:
            curEtf = etfDict[ticker]
            etfVals = curEtf.indicatorDict
            writer.writerow({
                'ticker': curEtf.ticker,
                'one_day_50': etfVals['one_day_50'],
                'one_day_200': etfVals['one_day_200'],
                'five_min_50': etfVals['five_min_50'],
                'five_min_200': etfVals['five_min_200'],
                'one_min_50': etfVals['one_min_50'],
                'one_min_200': etfVals['one_min_200'],
                'close_price': etfVals['close_price']
            })
    if (config.DEBUG):
        print(f'saving csv file as {config.CSVFILE}')

