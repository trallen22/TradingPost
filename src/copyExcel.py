'''
This script copies the template excel file from configurationFile.py and 
creates the new excel for current day based on generated csv
'''

import shutil
import csv
import openpyxl 
import configurationFile as config

# TODO16: figure out coloring for output platform 
def generate_tp():

    tickerIndex = {}

    # loading platform as workbook object
    platform = openpyxl.load_workbook(config.OUTPUTPLATFORM)
    platformSheet = platform.active

    # makes a copy of the template excel file
    shutil.copyfile(config.TEMPEXCEL, config.OUTPUTEXCEL)

    # loading excel as workbook object
    workbook = openpyxl.load_workbook(config.OUTPUTEXCEL)
    activeSheet = workbook.active

    # going through each cell and getting ticker index 
    for row in platformSheet.iter_rows(max_row=platformSheet.max_row, max_col=1):
        for cell in row:
            # gets the rows with tickers in the excel 
            if cell.value in config.TICKERS:
                tickerIndex[cell.value] = cell.coordinate[1:]

    for i in range(len(tickerIndex)):
        rowIndex = 6 + (i // 7) * 10
        colChar = chr(i % 7 + 67) # ascii 67 is 'C' 
        activeSheet[f'{colChar}{rowIndex}'] = config.TICKERS[i] # filling etf name cell 
        activeSheet[f'{colChar}{rowIndex + 8}'] = platformSheet[f'G{tickerIndex[config.TICKERS[i]]}'].value # close price 
        
    activeSheet['C11'].style = activeSheet['D11'].style

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

    # makes a copy of the template excel file
    shutil.copyfile(config.TEMPLATEPLATFORM, config.OUTPUTPLATFORM)

    # loading excel as workbook object
    workbook = openpyxl.load_workbook(config.OUTPUTPLATFORM)
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

    workbook.save(config.OUTPUTPLATFORM)

# generate_tp() # used for testing 