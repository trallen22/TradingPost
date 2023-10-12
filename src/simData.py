'''
This file simulates using the Trading Post on historical price data 

log numbers 700-799
'''

import configuration_file as config 
import datetime 
import os
import glob
import openpyxl 
import random 

AVAILABLEFUNDS = 20000
CURRANGE = 5 # number of days/months/years
TIMEUNIT = 365 # 365 to simulate a year 
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


def totalNetworth(portfolio, availableFunds, curSheet=None):
    if curSheet == None:
        workbook = openpyxl.load_workbook(f'{config.OUTROOT}/{config.STRYESTERDAY}_testTradingPost.xlsx')
        curSheet = workbook.active

    # TODO: find way to only go through tickers with at least one share 
    for ticker in list(portfolio.keys()):
        curBase = config.ETFBASECELL[ticker]
        charBase = curBase[0]
        numBase = int(curBase[1:])
        curClose = curSheet[f'{charBase}{numBase + 8}'].value # getting close price in tp 
        availableFunds += curClose * portfolio[ticker]

    return availableFunds

def simulate(curCash, curPortfolio, numSharesDict):
    # any file with "TradingPost" in the name 
    listFiles = glob.glob(f'{config.OUTROOT}/*TradingPost*')
    setFiles = set(listFiles)

    startDay = datetime.date.today() - datetime.timedelta(CURRANGE * TIMEUNIT + 1)

    for i in range(CURRANGE * TIMEUNIT):
        curDay = startDay + datetime.timedelta(i) 

        # filter out weekends (5 is saturday and 6 is sunday) 
        if not (curDay.weekday() == 5 or curDay.weekday() == 6):

            # config.logmsg('DEBUG', 700, f'current day is {curDay}')
            curFile = f'{config.OUTROOT}/{curDay}_testTradingPost.xlsx'
            # check if a trading post has already been generated for curDay
            if (curFile) in setFiles:
                pass
#                config.logmsg('DEBUG', 701, f'Trading Post already created for {curDay}')
            else:
                config.logmsg('NOTICE', 702, f'creating Trading Post for {curDay}')
                try:
                    # running the main.py trading post script to generate 
                    os.system(f'python3 {config.SRCROOT}/main.py -d -t {curDay}')
                except:
                    config.logmsg('ERROR', 703, f'failed to generate Trading Post for {curDay}')

            workbook = openpyxl.load_workbook(curFile)
            activeSheet = workbook.active

            buyDict = {}
            sellDict = {}

            for ticker in config.TICKERS:
                curBase = config.ETFBASECELL[ticker]
                charBase = curBase[0]
                numBase = int(curBase[1:])
                tempSignal = activeSheet[f'{charBase}{numBase + 5}'].value # Buy/Sell/Hold signal 
                curSignal = '' if (tempSignal == None) else tempSignal
                curClose = activeSheet[f'{charBase}{numBase + 8}'].value # setting close price in tp 

                if ('buy' in curSignal.lower()):
                    buyDict[ticker] = curClose
                elif ('sell' in curSignal.lower()):
                    sellDict[ticker] = curClose

            curAccountBalance = totalNetworth(numSharesDict, curCash, activeSheet)

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

            # sellDict is ticker and current price { ticker : current price }
            for key in sellDict:
                if (len(curPortfolio[key]) > 0): 
                    numSell, curPortfolio[key] = determineSell(curPortfolio[key], sellDict[key])
                    numSell = min(numSell, numSharesDict[key]) # make sure we don't sell shares we don't have. 
                    curCash += numSell * sellDict[key]
                    numSharesDict[key] -= numSell
                    config.logmsg('DEBUG', 705, f'selling {numSell} shares of {key} at {sellDict[key]} on {curDay}')

        else:
            pass 
#            config.logmsg('DEBUG', 706, f'skipping Trading Post for {curDay} because weekday = {curDay.weekday()}')

    return curCash, curPortfolio, numSharesDict

funds, portfolio, numShares = simulate(AVAILABLEFUNDS, CURPORTFOLIO, NUMSHARESDICT)

net = totalNetworth(numShares, funds)

print(f'initial amount: {AVAILABLEFUNDS}')
print(f'final net: {round(net, 2)}')
print(f'percent growth: {round(((net - AVAILABLEFUNDS) / AVAILABLEFUNDS) * 100, 2)}%')
print(f'current cash: {round(funds, 2)}')

# for ticker in config.TICKERS:
#     print(f'current portfolio for {ticker}:\n {portfolio[ticker]}')
