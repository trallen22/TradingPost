'''
This script copies the template excel file from configurationFile.py and 
creates the new excel for current day based on generated csv
'''

import shutil
import csv
import openpyxl 
import configurationFile as config

OUTPUTFILE = config.OUTPUTEXCELFILE
LISTTICKERS = config.TICKERS
CURCSV = config.CSVFILE
DATE = config.TODAYDATE
COLUMNS = config.INPUTS

tickerDict = {} 
tickerIndex = {}

# Reads through csv file created by generate_csv.py
with open(CURCSV) as csv_file:
    rowReader = csv.DictReader(csv_file)
    for row in rowReader:
        tickerDict[row['ticker']] = row

# makes a copy of the template excel file
shutil.copyfile(config.TEMPLATEEXCELFILE, OUTPUTFILE)

# loading excel as workbook object
workbook = openpyxl.load_workbook(OUTPUTFILE)
activeSheet = workbook.active

# going through each cell and getting ticker index 
for row in activeSheet.iter_rows(max_row=activeSheet.max_row, max_col=1):
    for cell in row:
        # gets the rows with tickers in the excel 
        if cell.value in LISTTICKERS:
            tickerIndex[cell.coordinate[1:]] = cell.value

# populates the input values for the current excel
for index in tickerIndex:
    curTicker = tickerIndex[index] 
    activeSheet[f'E{index}'] = DATE # sets the date in column 'E'
    for letterCoord in COLUMNS:
        # autofills with column keys from INPUTS in configurationFile.py
        activeSheet[f'{letterCoord}{index}'] = float(tickerDict[curTicker][COLUMNS[letterCoord]])

workbook.save(OUTPUTFILE)
