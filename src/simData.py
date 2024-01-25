'''
This file simulates using the Trading Post on historical price data 

log numbers 700-799
'''

from ast import Name
import configuration_file as config 
import datetime 
import os
import glob
import random 
import csv 
import matplotlib.pyplot as plt
from tqdm import tqdm
from sortedcontainers import SortedList
from statistics import mean, median

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
        curCsvPath = f"{config.OUTROOT}/outFiles/{config.STRYESTERDAY}_csv.csv"
    # TODO: need to add try/except block 
    with open(curCsvPath, 'r') as curFile:
        curCsv = csv.DictReader(curFile)
        for row in curCsv:
            availableFunds += float(row['close_price']) * portfolio[row['ticker']]
    return availableFunds

def simulate(curCash, curRange=5, timeUnit=365):
    startingCash = curCash
    numSharesDict = {} # dictionary of number of shares for each ticker { ticker : 3 (# shares) }
    curPortfolio = {} # nested dictionary simulating portfolio { ticker : { buy price : number of shares } }
    for ticker in config.TICKERS:
        curPortfolio[ticker] = {}
        numSharesDict[ticker] = 0

    listDailyNetValue = []
    listDates = []
    curAccountBalance = curCash # will need to change this if want to start with non-empty portfolio 
    # very convoluted dictionary for dictMonthlyPrices 
    # dMP = { 
    #       year : {
    #               month : {
    #                       sum (of net worth for each day) : int, 
    #                       min (net worth for the month): int, 
    #                       max (net worth for the month) : int, 
    #                       sortedList (of days; used for median) : SortedList 
    #                       }
    #               month2 : ...
    #               }     
    #       year2 : ...
    #   }
    dictMonthlyPrices = {} 

    # all the csv files 
    listFiles = glob.glob(f'{config.OUTROOT}/outFiles/*.csv')
    setFiles = set(listFiles)

    startDay = datetime.date.today() - datetime.timedelta(curRange * timeUnit)

    for i in range(curRange * timeUnit):
        curDay = startDay + datetime.timedelta(i) 

        # filter out weekends (5 is saturday and 6 is sunday) 
        if not (curDay.weekday() == 5 or curDay.weekday() == 6):
            curFilePath = f'{config.OUTROOT}/outFiles/{curDay}_csv.csv'
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
            skipDay = 0

            # TODO: need to add try/except 
            with open(curFilePath, 'r') as curFile:
                curCsv = csv.DictReader(curFile)
                for row in curCsv:
                    if (float(row['close_price']) < 0): 
                        config.logmsg('DEBUG', 708, f'Found negative close price on {curDay}, skipping buy/sell')
                        skipDay = 1
                        break 
                    if ('buy' in row['signal'].lower()):
                        buyDict[row['ticker']] = float(row['close_price'])
                        if (float(row['close_price']) < 0): 
                            config.logmsg('ERROR', 709, f'negative buy value')
                    elif ('sell' in row['signal'].lower()):
                        sellDict[row['ticker']] = float(row['close_price'])
                        if (float(row['close_price']) < 0): 
                            config.logmsg('ERROR', 710, f'negative sell value')
            if not (skipDay): 
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

                curAccountBalance = round(totalNetworth(numSharesDict, curCash, curFilePath), 2)
                listDailyNetValue.append(curAccountBalance)
                listDates.append(curDay)
                config.logmsg('DEBUG', 707, f'Account Balance on {curDay} = {curAccountBalance}')

                onlyYear = str(curDay)[:4]
                onlyMonth = str(curDay)[5:7]
                # checking if current year is in the dictionary yet 
                try:
                    dictMonthlyPrices[onlyYear]
                except KeyError:
                    # TODO: Could try to make this similar to monthly nested dict to try and get per year data 
                    # TODO: for mean could could sum over sortedClosePrices for each month 
                    dictMonthlyPrices[onlyYear] = {} 
                # checking if current month is in the year's nested dict 
                try: 
                    dictMonthlyPrices[onlyYear][onlyMonth]
                except KeyError:
                    dictMonthlyPrices[onlyYear][onlyMonth] = { 'numDays': 0, 'startPrice': curAccountBalance, 'monthSumNet': 0, 'monthMin': 1000000, 'monthMax': -1, 'sortedClosePrices': SortedList() }
                # filling dMP 
                dictMonthlyPrices[onlyYear][onlyMonth]['monthSumNet'] += curAccountBalance
                if (curAccountBalance < dictMonthlyPrices[onlyYear][onlyMonth]['monthMin']):
                    dictMonthlyPrices[onlyYear][onlyMonth]['monthMin'] = curAccountBalance
                elif (curAccountBalance > dictMonthlyPrices[onlyYear][onlyMonth]['monthMax']): 
                    dictMonthlyPrices[onlyYear][onlyMonth]['monthMax'] = curAccountBalance
                dictMonthlyPrices[onlyYear][onlyMonth]['sortedClosePrices'].add(curAccountBalance)
        else:
            config.logmsg('DEBUG', 706, f'skipping Trading Post for {curDay} because weekday = {curDay.weekday()}')

    gen_monthly_sim_csv(dictMonthlyPrices, startingCash)
    return listDailyNetValue, listDates 

def gen_monthly_sim_csv(dictMonthlyVals, initialCash):
    monthCsvFile = f"/Users/tristanallen/Desktop/TradingPost/visuals/testSimMonthlyReport.csv"
    yearlyCsvFile = f"/Users/tristanallen/Desktop/TradingPost/visuals/testSimYearlyReport.csv"
    with open(monthCsvFile, mode='w') as curCsv, open(yearlyCsvFile, mode='w') as yearCsv:
        fieldNames = ['month', 'month_min', 'month_max', 'mean_price', 'median_price', 'start_price', 'month_over_month', 'start_to_date']
        monthWriter = csv.DictWriter(curCsv, fieldnames=fieldNames)
        monthWriter.writeheader() 
        # yearWriter = csv.DictWriter(yearCsv, fieldnames=fieldNames)
        # yearWriter.writeheader()
        for year in list(dictMonthlyVals.keys()):
            for month in dictMonthlyVals[year]:
                curNumDays = len(dictMonthlyVals[year][month]['sortedClosePrices'])
                curMean = dictMonthlyVals[year][month]['monthSumNet'] / curNumDays
                sortedPrice = list(dictMonthlyVals[year][month]['sortedClosePrices'])
                midIndex = curNumDays // 2
                if curNumDays % 2 == 1:
                    curMedian = sortedPrice[midIndex]
                else: 
                    curMedian = ((sortedPrice[midIndex - 1] + sortedPrice[midIndex]) / 2)
                curMonthStart = dictMonthlyVals[year][month]['startPrice']
                try: 
                    monthOverMonth = ((curMonthStart - prevMonthStart) / prevMonthStart) * 100 
                except NameError:
                    prevMonthStart = curMonthStart
                    monthOverMonth = 0
                yearToDate = ((curMonthStart - initialCash) / initialCash) * 100
                monthWriter.writerow({
                    'month': f"{year}-{month}", 
                    'month_min': dictMonthlyVals[year][month]['monthMin'], 
                    'month_max': dictMonthlyVals[year][month]['monthMax'], 
                    'mean_price': round(curMean, 2), 
                    'median_price': round(curMedian, 2), 
                    'start_price': curMonthStart, 
                    'month_over_month': round(monthOverMonth, 2),
                    'start_to_date': round(yearToDate, 2)
                })
                prevMonthStart = curMonthStart
            

def generate_sim_chart(listDailyVals, listDates):
    for i in range(len(listDailyVals)): 
        plt.plot(listDates[i], listDailyVals[i], linewidth=0.5)
    plt.ylabel("net value")
    plt.xlabel("year")
    plt.ylim(ymin=0)
    plt.grid(True)
    plt.savefig(f"/Users/tristanallen/Desktop/TradingPost/visuals/testGraph.pdf")

def run_simulation(): 
    listDailyVals = []
    listDates = []
    tryCash = 1
    while (tryCash): 
        try: 
            initialCash = int(input("How much cash to start with: "))
            tryCash = 0
        except ValueError:
            print("invalid value, please enter positive integer")
    tryNumSims = 1
    while (tryNumSims):
        try: 
            numSims = int(input("How many simulations: "))
            tryNumSims = 0
        except ValueError:
            print("invalid value, please enter positive integer")
    pbar = tqdm(desc='simulations ran', total=numSims)
    for i in range(numSims): 
        DailyVals, Dates = simulate(initialCash)
        listDailyVals.append(DailyVals)
        listDates.append(Dates)
        pbar.update(1)
    pbar.close()
    generate_sim_chart(listDailyVals, listDates)
