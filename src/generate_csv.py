'''
This script generates a csv from a dictionary of etf objects
'''

import csv
import configurationFile as config

# generate_csv: generates a csv file with path config.CSVFILE
# parameters: 
#       etfDict - a dictionary of etf objects 
#       csvFile - the output csv file 
# returns:  0 - successfully generated csv file
#           1 - failed 
def generate_csv(etfDict, csvFile):
    try: 
        with open(csvFile, mode='w') as curCsv:
            fieldnames = ['ticker', 'one_day_50',
                            'one_day_200', 'five_min_50', 
                            'five_min_200','one_min_50', 
                            'one_min_200', 'close_price']
            writer = csv.DictWriter(curCsv, fieldnames=fieldnames)
            writer.writeheader()
            for ticker in config.TICKERS:
                curEtf = etfDict[ticker]
                etfVals = curEtf.indicatorDict
                config.logmsg('DEBUG', 430 + config.TICKERS.index(ticker), f'writing csv row for {ticker}')
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
        config.logmsg('DEBUG', 400, f'saving csv file as {csvFile}')
    except Exception as e:
        config.logmsg('ERROR', 401, f'{e}')
        return 1
    return 0

