'''
This file simulates using the Trading Post on historical price data 

log numbers 700-799
'''

import configuration_file as config 
import datetime 
import os
import glob
import random 
import csv 

AVAILABLEFUNDS = 20000
CURRANGE = 5 # number of time units
TIMEUNIT = 365 # number of days; 365 to simulate a year 
NUMSHARESDICT = {}
CURPORTFOLIO = {} # nested dictionary simulating portfolio { ticker : { buy price : number of shares } }
for ticker in config.TICKERS:
    CURPORTFOLIO[ticker] = {}
    NUMSHARESDICT[ticker] = 0

def determineSell(etfPortfolioDict, sellPrice):
    buyPrice = 0
    maxReturn = -10000000
    for price in etfPortfolioDict:
        curReturn = sellPrice - price
        if curReturn > maxReturn:
            maxReturn = curReturn 
            buyPrice = price 
    # returns the number of shares from best price (lot of shares) to sell 
    return etfPortfolioDict.pop(buyPrice), etfPortfolioDict


def totalNetworth(portfolio, availableFunds, curCsvPath=None):
    if curCsvPath == None:
        curCsvPath = f"{config.OUTROOT}/{config.STRYESTERDAY}_csv.csv"
    # TODO: need to add try/except block 
    with open(curCsvPath, 'r') as curFile:
        curCsv = csv.DictReader(curFile)
        for row in curCsv:
            availableFunds += float(row['close_price']) * portfolio[row['ticker']]
    return availableFunds

def simulate(curCash, curPortfolio, numSharesDict):
    # all the csv files 
    listFiles = glob.glob(f'{config.OUTROOT}/*.csv')
    setFiles = set(listFiles)

    startDay = datetime.date.today() - datetime.timedelta(CURRANGE * TIMEUNIT)

    for i in range(CURRANGE * TIMEUNIT):
        curDay = startDay + datetime.timedelta(i) 

        # filter out weekends (5 is saturday and 6 is sunday) 
        if not (curDay.weekday() == 5 or curDay.weekday() == 6):
            curFilePath = f'{config.OUTROOT}/outfiles/{curDay}_csv.csv'
            # check if a trading post has already been generated for curDay
            if (curFilePath) in setFiles:
                config.logmsg('DEBUG', 701, f'Trading Post already created for {curDay}')
            else:
                config.logmsg('NOTICE', 702, f'creating historical post for {curDay}')
                try:
                    # running the main.py trading post script to generate 
                    os.system(f'python3 {config.SRCROOT}/main.py -c -d -t {curDay}')
                except:
                    config.logmsg('ERROR', 703, f'failed to generate historical post for {curDay}')

            buyDict = {}
            sellDict = {}

            # TODO: need to add try/except 
            with open(curFilePath, 'r') as curFile:
                curCsv = csv.DictReader(curFile)
                for row in curCsv:
                    if ('buy' in row['signal'].lower()):
                        buyDict[row['ticker']] = float(row['close_price'])
                    elif ('sell' in row['signal'].lower()):
                        sellDict[row['ticker']] = float(row['close_price'])

            curAccountBalance = totalNetworth(numSharesDict, curCash, curFilePath)
            config.logmsg('DEBUG', 707, f'Account Balance on {curDay} = {curAccountBalance}')

            # sellDict is ticker and current price { ticker : current price }
            for key in sellDict:
                if (len(curPortfolio[key]) > 0): 
                    numSell, curPortfolio[key] = determineSell(curPortfolio[key], sellDict[key])
                    numSell = min(numSell, numSharesDict[key]) # make sure we don't sell shares we don't have. 
                    curCash += numSell * sellDict[key]
                    numSharesDict[key] -= numSell
                    config.logmsg('DEBUG', 705, f'selling {numSell} shares of {key} at {sellDict[key]} on {curDay}')

            buyKeys = list(buyDict.keys()) 
            random.shuffle(buyKeys) # shuffling prevents always buying same etfs first 
            for key in buyKeys:
                numBuy = max(((curAccountBalance * 0.01) // buyDict[key]), 1)
                if numBuy * buyDict[key] < curCash: 
                    curCash -= numBuy * buyDict[key]
                    try: 
                        curPortfolio[key][buyDict[key]] += numBuy # this looks like { JNK : { $20:2, $30:1 } }
                    except Exception: 
                        curPortfolio[key][buyDict[key]] = numBuy
                    numSharesDict[key] += numBuy
                    config.logmsg('DEBUG', 704, f'buying {numBuy} shares of {key} at {buyDict[key]} on {curDay}')

        else:
            config.logmsg('DEBUG', 706, f'skipping Trading Post for {curDay} because weekday = {curDay.weekday()}')

    return curCash, curPortfolio, numSharesDict

funds, portfolio, numShares = simulate(AVAILABLEFUNDS, CURPORTFOLIO, NUMSHARESDICT)

net = totalNetworth(numShares, funds)

print(f'initial amount: {AVAILABLEFUNDS}')
print(f'final net: {round(net, 2)}')
print(f'percent growth: {round(((net - AVAILABLEFUNDS) / AVAILABLEFUNDS) * 100, 2)}%')
print(f'current cash: {round(funds, 2)}')

# for ticker in config.TICKERS:
#     print(f'current portfolio for {ticker}:\n {portfolio[ticker]}')
