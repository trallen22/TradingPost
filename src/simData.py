'''
This file simulates using the Trading Post on historical price data 

log numbers 700-799
'''

import configuration_file as config 
import datetime 
import os
import glob
import openpyxl 

AVAILABLEFUNDS = 20000
CURRANGE = 5 # number of days/months/years
TIMEUNIT = 365 # 365 to simulate a year 

CURPORTFOLIO = {} # dictionary simulating portfolio { ticker : number of shares }
for ticker in config.TICKERS:
    CURPORTFOLIO[ticker] = 0

def totalNetworth(portfolio, availableFunds):
    workbook = openpyxl.load_workbook(f'{config.OUTROOT}/2023-10-09_testTradingPost.xlsx')
    activeSheet = workbook.active

    for ticker in config.TICKERS:
        curBase = config.ETFBASECELL[ticker]
        charBase = curBase[0]
        numBase = int(curBase[1:])
        curClose = activeSheet[f'{charBase}{numBase + 8}'].value # setting close price in tp 
        availableFunds += curClose * portfolio[ticker]

    return availableFunds

def simulate(curTotalPortfolioValue, curPortfolio, initialFunds):
    # any file with "TradingPost" in the name 
    listFiles = glob.glob(f'{config.OUTROOT}/*TradingPost*')

    startDay = datetime.date.today() - datetime.timedelta(CURRANGE * TIMEUNIT)

    for i in range(CURRANGE * TIMEUNIT):
        curDay = startDay + datetime.timedelta(i) 

        # filter out weekends (5 is saturday and 6 is sunday) 
        if not (curDay.weekday() == 5 or curDay.weekday() == 6):

            config.logmsg('DEBUG', 700, f'current day is {curDay}')
            curFile = f'{config.OUTROOT}/{curDay}_testTradingPost.xlsx'
            # check if a trading post has already been generated for curDay
            if (curFile) in listFiles:
                config.logmsg('DEBUG', 701, f'Trading Post already created for {curDay}')
            # if trading post is not already generated for curDay 
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

            for key in buyDict:
                numBuy = max(((initialFunds * 0.01) // buyDict[key]), 1)
                # print(f'etf: {key}')
                # print(f'close: {buyDict[key]}')
                # print(f'1%: {curTotalPortfolioValue * 0.01}')
                # print(f'num: {numBuy}')
                # print()

                if numBuy * buyDict[key] < curTotalPortfolioValue: 
                    curTotalPortfolioValue -= numBuy * buyDict[key]
                    curPortfolio[key] += numBuy
                    config.logmsg('DEBUG', 704, f'buying {numBuy} shares of {key}')

            for key in sellDict:
                # print(f'etf: {key}')
                # print(f'close: {sellDict[key]}')
                # print()

                if curPortfolio[key] > 0: 
                    curTotalPortfolioValue += sellDict[key]
                    curPortfolio[key] -= 1
                    config.logmsg('DEBUG', 705, f'selling {key}')
        else: 
            config.logmsg('DEBUG', 706, f'skipping Trading Post for {curDay} because weekday = {curDay.weekday()}')

        # print('current portfolio')
        # print(curPortfolio)

    return curTotalPortfolioValue, curPortfolio 

        

funds, portfolio = simulate(AVAILABLEFUNDS, CURPORTFOLIO, AVAILABLEFUNDS)

net = totalNetworth(portfolio, funds)

print(f'final net: {net}')
print(f'percent growth: {round(((net - AVAILABLEFUNDS) / AVAILABLEFUNDS) * 100, 2)}%')
print(f'current cash: {funds}')
print(f'current portfolio: {portfolio}')
