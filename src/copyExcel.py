'''
This script copies the template excel file from configurationFile.py and 
creates the new excel for current day based on generated csv
'''

import shutil
import csv
import time
import openpyxl 
import configurationFile as config
import platFormulas as formula
# from koala.ExcelCompiler import ExcelCompiler
# from koala.Spreadsheet import Spreadsheet


# TODO19: Implement set_ranges 
def set_ranges(rangeType, etf):
    if rangeType == 'buy':
        rangeMin = formula.buy_min(etf)
        rangeMax = formula.buy_max(etf)
    elif rangeType == 'sell':
        rangeMin = formula.sell_min(etf)
        rangeMax = formula.sell_max(etf)
    else:
        return '', ''
    if rangeMin < rangeMax:
        return rangeMin, rangeMax 
    return rangeMax, rangeMin 

# def determine_buy_sell(platformSheet, excelSheet, platRow, signalRow, tpCol):
#     signalCell = excelSheet[f'{tpCol}{signalRow}']
#     tpRangeRow = [signalRow + 1, signalRow + 2]
#     if (platformSheet[f'G{platRow}'].value > platformSheet[f'H{platRow}'].value):
#         # Looking for sell signals 
#         if (platformSheet[f'G{platRow}'].value > platformSheet[f'I{platRow}'].value):
#             minPrice = 1000000000
#             for col in [ 'J', 'K', 'L', 'M' ]:
#                 minPrice = min(minPrice, platformSheet[f'{col}{platRow}'].value)
#             if (platformSheet[f'G{platRow}'].value < minPrice):
#                 signalCell.value = '!SELL!'
#                 signalCell.fill = config.SELLCOLOR
#             else:
#                 signalCell.value = 'HOLD'
#                 signalCell.fill = config.HOSELLCOLOR
#             rangeCols = [ 'Z', 'AA' ]
#             set_ranges(platformSheet, excelSheet, tpCol, tpRangeRow, rangeCols, platRow)
#             return 
#     else:
#         # Looking for buy signals 
#         if (platformSheet[f'G{platRow}'].value < platformSheet[f'I{platRow}'].value):
#             maxPrice = -1
#             for col in [ 'J', 'K', 'L', 'M' ]:
#                 maxPrice = max(maxPrice, platformSheet[f'{col}{platRow}'].value)
#             if (platformSheet[f'G{platRow}'].value > maxPrice):
#                 signalCell.value = '!BUY!'
#                 signalCell.fill = config.BUYCOLOR
#             else:
#                 signalCell.value = 'HOLD'
#                 signalCell.fill = config.HOBUYCOLOR
#             rangeCols = [ 'X', 'Y' ]
#             set_ranges(platformSheet, excelSheet, tpCol, tpRangeRow, rangeCols, platRow)
#             return 
#     signalCell.value = 'HOLD'
#     signalCell.fill = config.PLAINCOLOR
#     set_ranges(platformSheet, excelSheet, tpCol, tpRangeRow, [], platRow, clearCells=True)


def determine_buy_sell(etf):
    etfVals = etf.indicatorDict
    if (etfVals['close_price'] > etfVals['one_day_50']):
        # Looking for sell signals 
        if (etfVals['close_price'] > etfVals['one_day_200']):
            minPrice = 1000000000
            for col in config.MINDICATORS:
                minPrice = min(minPrice, etfVals[col])
            if (etfVals['close_price'] < minPrice):
                return '!SELL!', config.SELLCOLOR, 'sell'
            else:
                return 'HOLD', config.HOSELLCOLOR, 'sell'
            # rangeCols = [ 'Z', 'AA' ]
            # set_ranges(platformSheet, excelSheet, tpCol, tpRangeRow, rangeCols, platRow)
            # return 
    else:
        # Looking for buy signals 
        if (etfVals['close_price'] < etfVals['one_day_50']):
            maxPrice = -1
            for col in config.MINDICATORS:
                maxPrice = max(maxPrice, etfVals[col])
            if (etfVals['close_price'] > maxPrice):
                return '!BUY!', config.BUYCOLOR, 'buy'
            else:
                return 'HOLD', config.HOBUYCOLOR, 'buy'
            # rangeCols = [ 'X', 'Y' ]
            # set_ranges(platformSheet, excelSheet, tpCol, tpRangeRow, rangeCols, platRow)
            # return 
    return 'HOLD', config.PLAINCOLOR, ''
    # set_ranges(platformSheet, excelSheet, tpCol, tpRangeRow, [], platRow, clearCells=True)


# TODO16: figure out coloring for output platform 
def generate_tp():

    tickerIndex = {}

    # TODO21: work on getting value instead of formula 
    
    # USED FOR DEMO 
    platform = openpyxl.load_workbook(config.OUTPUTPLATFORM)
    platform['Sheet1']['AL1'].value = 100
    platform.save(config.OUTPUTPLATFORM)
    platform.close()
    platform = openpyxl.load_workbook(config.OUTPUTPLATFORM, data_only=True)
    platformSheet = platform.active
    

    # makes a copy of the template excel file
    shutil.copyfile(config.TEMPEXCEL, config.OUTPUTEXCEL)

    # loading excel as workbook object
    workbook = openpyxl.load_workbook(config.OUTPUTEXCEL)
    excelSheet = workbook.active

    # going through each cell and getting ticker index 
    for row in platformSheet.iter_rows(max_row=platformSheet.max_row, max_col=1):
        for cell in row:
            # gets the rows with tickers in the excel 
            if cell.value in config.TICKERS:
                tickerIndex[cell.value] = cell.coordinate[1:]

    for i in range(len(tickerIndex)):
        tickerRow = 7 + (i // 7) * 10
        signalRow = tickerRow + 5
        colChar = chr(i % 7 + 67) # tp column ETF coordinate; ascii 67 is 'C' 
        excelSheet[f'{colChar}{tickerRow}'] = config.TICKERS[i] # filling etf name cell 
        excelSheet[f'{colChar}{tickerRow + 3}'] = config.TODAYDATE # filling today date 
        excelSheet[f'{colChar}{tickerRow + 8}'] = platformSheet[f'G{tickerIndex[config.TICKERS[i]]}'].value # close price 
        determine_buy_sell(platformSheet, excelSheet, tickerIndex[config.TICKERS[i]], signalRow, colChar)

    if (config.DEBUG):
        print(f'saving trading post as {config.OUTPUTEXCEL}')

    workbook.save(config.OUTPUTEXCEL)

# TODO15: add parameters to fill_excel
def fill_excel():

    tickerDict = {} 
    tickerIndex = {}

    # Reads through csv file created by generate_csv.py
    with open(config.CSVFILE) as csv_file:
        rowReader = csv.DictReader(csv_file)
        for row in rowReader:
            tickerDict[row['ticker']] = row

    # makes a copy of the template platform file
    shutil.copyfile(config.TEMPLATEPLATFORM, config.OUTPUTPLATFORM)

    # loading excel as workbook object
    workbook = openpyxl.load_workbook(config.OUTPUTPLATFORM, data_only=False)
    activeSheet = workbook.active

    # going through each cell and getting ticker index 
    for row in activeSheet.iter_rows(max_row=activeSheet.max_row, max_col=1):
        for cell in row:
            # gets the rows with tickers in the excel 
            if cell.value in config.TICKERS:
                tickerIndex[cell.coordinate[1:]] = cell.value

    # populates the input values for the current excel
    for index in tickerIndex:
        curTicker = tickerIndex[index] 
        activeSheet[f'E{index}'] = config.TODAYDATE # sets the date in column 'E' 
        for letterCoord in config.INPUTS: 
            # autofills with column keys from INPUTS in configurationFile.py 
            activeSheet[f'{letterCoord}{index}'] = float(tickerDict[curTicker][config.INPUTS[letterCoord]])

    if (config.DEBUG):
        print(f'created temp platform {config.OUTPUTPLATFORM}')

    workbook.save(config.OUTPUTPLATFORM)
    workbook.close()

    # shutil.copyfile(config.OUTPUTPLATFORM, config.RAWPLATFORM)
    # raw = openpyxl.load_workbook(config.OUTPUTPLATFORM, data_only=False)
    # print(raw['Sheet1']['X6'].value)
    # raw.save(config.RAWPLATFORM)
    # raw.close()
    # raw = openpyxl.load_workbook(config.RAWPLATFORM, data_only=True)
    # rawSheet = raw.active
    # print(rawSheet['X6'].value)
    # raw.save(config.RAWPLATFORM)
    # raw.close()

    # print(config.OUTPUTPLATFORM)

    # ### Graph Generation ###
    # c = ExcelCompiler(config.OUTPUTPLATFORM)
    # sp = c.gen_graph()

    # ## Graph Serialization ###
    # print("Serializing to disk...")
    # sp.dump(config.OUTPUTPLATFORM.replace("xlsx", "gzip"))

    # ### Graph Loading ###
    # print("Reading from disk...")
    # sp = Spreadsheet.load(config.OUTPUTPLATFORM.replace("xlsx", "gzip"))

    # ### Graph Evaluation ###
    # sp.set_value('Sheet1!A1', 10)
    # print('New D1 value: %s' % str(sp.evaluate('Sheet1!D1')))


    # workbook.close()
