import multiprocessing
import openpyxl 
import shutil 
from tqdm import tqdm
from etf import Etf 
import configuration_file as config
from copy_excel import determine_buy_sell, fill_platform
from generate_csv import generate_csv
from send_email import send_email
import os
import sys
from sys import exit

multiprocessing.freeze_support() # prevents multithreading in pyinstaller --onedir
os.system('clear')

etfDict = {} # { str ticker : etf object }

# if (config.GETVALUE):
#     if (len(sys.argv) != 6): # USAGE: main.py -v 'ticker' 'interval' 'timefram' 'date'
#         print('Error: usage')
#         exit(21)
#     etfDict[sys.argv[2]] = Etf(sys.argv[2], 'value')
#     curDir = config.TPROOT

#     exit(90)

if (config.PBAR):
    pBar = tqdm(desc='tickers found', total=len(config.TICKERS))
for ticker in config.TICKERS:
    # creates a dictionary of Etf objects 
    etfDict[ticker] = Etf(ticker, 'name') # implement names -> 'HighYieldBonds' 
    if (config.PBAR):
        pBar.update(1)
if (config.PBAR):
    pBar.close()

# makes a copy of the template platform file
try:
    shutil.copyfile(config.TEMPEXCEL, config.OUTPUTEXCEL)
except FileNotFoundError as e:
    if (config.DEBUG):
        print(e)
        print(f'creating file {config.OUTPUTEXCEL}')
        exit(9)

# loading excel as workbook object
workbook = openpyxl.load_workbook(config.OUTPUTEXCEL)
activeSheet = workbook.active

for ticker in config.TICKERS:
    curEtf = etfDict[ticker]
    curBase = curEtf.basecell
    charBase = curBase[0]
    numBase = int(curBase[1:])

    activeSheet[curBase] = curEtf.ticker # setting ticker name in tp
    activeSheet[f'{charBase}{numBase + 1}'].value = curEtf.name # setting etf name in tp 
    activeSheet[f'{charBase}{numBase + 3}'] = config.TODAYDATE # setting today date in tp 

    signal, sigColor, minTradeRange, maxTradeRange = determine_buy_sell(curEtf)
    activeSheet[f'{charBase}{numBase + 5}'] = signal # Buy/Sell/Hold signal 
    activeSheet[f'{charBase}{numBase + 5}'].fill = sigColor # Buy/Sell/Hold color 
    
    activeSheet[f'{charBase}{numBase + 6}'] = minTradeRange
    activeSheet[f'{charBase}{numBase + 7}'] = maxTradeRange
    activeSheet[f'{charBase}{numBase + 8}'] = curEtf.indicatorDict['close_price'] # setting close price in tp 

if (config.CSV):
    if(generate_csv(etfDict, config.CSVFILE)):
        config.logmsg('ERROR', 103, 'unable to generate CSV')
    else:
        config.logmsg('INFO', 104, f'saved csv file to {config.CSVFILE}')

if (config.FILLPLATFORM):
    try:
        fill_platform(etfDict) 
    except Exception as e:
        config.logmsg('ERROR', 101, f'{e}')
        config.logmsg('NOTICE', 102, 'unable to generate Platform')

workbook.save(config.OUTPUTEXCEL)
if (config.DEBUG):
    print(f'saving trading post as {config.OUTPUTEXCEL}')
workbook.close()

if (config.SENDEMAIL):
    send_email(config.EMAILLIST[0], 'Todays Trading Post', 'This is for the demo')