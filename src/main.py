import openpyxl 
import shutil 
import time
from tqdm import tqdm
from etf import Etf 
import configurationFile as config
from copyExcel import determine_buy_sell, set_ranges, fill_platform
from generate_csv import generate_csv

etfDict = {} # { str ticker : etf object }

if (config.PBAR):
    pBar = tqdm(desc='tickers found', total=len(config.TICKERS))
for ticker in config.TICKERS:
    # creates a dictionary of Etf objects 
    etfDict[ticker] = Etf(ticker, 'name') # implement names -> 'HighYieldBonds' 
    if (config.PBAR):
        pBar.update(1)
    # ensure we don't pass 5 API calls/min for polygon 
    if not (ticker == config.TICKERS[-1]):
        time.sleep(60)
if (config.PBAR):
    pBar.close()

# makes a copy of the template platform file
shutil.copyfile(config.TEMPEXCEL, config.OUTPUTEXCEL)

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

    signal, sigColor, rangeType = determine_buy_sell(curEtf)
    activeSheet[f'{charBase}{numBase + 5}'] = signal # Buy/Sell/Hold signal 
    activeSheet[f'{charBase}{numBase + 5}'].fill = sigColor # Buy/Sell/Hold color 
    minTradeRange, maxTradeRange = set_ranges(rangeType, curEtf)
    activeSheet[f'{charBase}{numBase + 6}'] = minTradeRange
    activeSheet[f'{charBase}{numBase + 7}'] = maxTradeRange
    activeSheet[f'{charBase}{numBase + 8}'] = curEtf.indicatorDict['close_price'] # setting close price in tp 

if (config.CSV):
    generate_csv(etfDict)

if (config.FILLPLATFORM):
    fill_platform(curEtf)    

workbook.save(config.OUTPUTEXCEL)
if (config.DEBUG):
    print(f'saving trading post as {config.OUTPUTEXCEL}')
workbook.close()

