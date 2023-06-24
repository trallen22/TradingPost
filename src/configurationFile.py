'''
This file holds all the configuraion information
'''
from datetime import date
from polygon import RESTClient 
import os
import openpyxl

SRCPATH = os.path.dirname(__file__) + '/'

# convert todays date to mm/dd form 
today = date.today()

listDate = str(today).split('-')
TODAYDATE = f'{listDate[1]}/{listDate[2]}' 

STRTODAY = today.strftime('%Y-%m-%d') # used with polygon data

PRINTDF = 1 # prints dataframes to terminal
PBAR = 1 # print progress bar for polygon calls in generate_csv.py 
DEBUG = 1 # print debug messages # TODO20: add debug messages 

# polygon login 
'''Insert your key. Play around with the free tier key first.'''
key = "nGJdIcDOy3hzWwn6X6gritFJkgDWTpRJ"
CLIENT = RESTClient(key)

PARAMSET = [[ 'minute', 1 ], # one minute time interval 
                [ 'minute', 5 ], # 5 minute time interval 
                [ 'day', 1 ]] #one day time interval 

# Platform variables 
TEMPLATEPLATFORM = SRCPATH + 'TA.WORK.xlsx'
OUTPUTPLATFORM = SRCPATH + 'testPlatform.xlsx'
RAWPLATFORM = SRCPATH + 'rawPlatform.xlsx'

# Trading Post variables 
TEMPEXCEL = SRCPATH + 'stocktradingpost2.xlsx'
OUTPUTEXCEL = SRCPATH + 'testTradingPost.xlsx'

CSVFILE = SRCPATH + 'testCsv.csv' 

# TICKERS = ["JNK", "GDX", "VCR", "VDC", "VIG", "VDE", "VFH", 
#         "VWO", "VHT", "VIS", "VGT", "VAW", "VNQ", "VOO", 
#         "VOX", "BND", "BNDX", "VXUS", "VTI", "VPU", "XTN"]

TICKERS = ["JNK"] # used for testing 

INDICATORS = ['one_day_50', 'one_day_200', 'five_min_50', 'five_min_200', 'one_min_50', 'one_min_200', 'close_price']

INPUTS = { 'G':'last_price', 'H':'one_day_50', 'I':'one_day_200', 'J':'five_min_50', 
        'K':'five_min_200', 'L':'one_min_50', 'M':'one_min_200' }

try: 
        # loading excel as workbook object
        workbook = openpyxl.load_workbook(TEMPEXCEL)
        excelSheet = workbook.active
except Exception as e:
        print(f'ERROR: {e}')
        exit(4)

COLORROW = 5
plainRGB = 'FFFFFFFF'
PLAINCOLOR = openpyxl.styles.PatternFill(start_color=plainRGB, end_color=plainRGB, fill_type='solid')

# Cell color templates 
try:
        buyRGB = excelSheet[f'A{COLORROW}'].fill.fgColor
        BUYCOLOR = openpyxl.styles.PatternFill(start_color=buyRGB, end_color=buyRGB, fill_type='solid')
except Exception:
        BUYCOLOR = PLAINCOLOR
        print(f'NOTICE: Buy Color set as plain')
try:
        hoBuyRGB = excelSheet[F'C{COLORROW}'].fill.fgColor
        HOBUYCOLOR = openpyxl.styles.PatternFill(start_color=hoBuyRGB, end_color=hoBuyRGB, fill_type='solid')
except Exception:
        HOBUYCOLOR = PLAINCOLOR
        print(f'NOTICE: Hold to Buy Color set as plain')
try:
        sellRGB = excelSheet[f'E{COLORROW}'].fill.fgColor
        SELLCOLOR = openpyxl.styles.PatternFill(start_color=sellRGB, end_color=sellRGB, fill_type='solid')
except Exception:
        SELLCOLOR = PLAINCOLOR
        print(f'NOTICE: Sell Color set as plain')
try:
        hoSellRGB = excelSheet[f'F{COLORROW}'].fill.fgColor
        HOSELLCOLOR = openpyxl.styles.PatternFill(start_color=hoSellRGB, end_color=hoSellRGB, fill_type='solid')
except Exception:
        HOSELLCOLOR = PLAINCOLOR
        print(f'NOTICE: Hold to Sell Color set as plain')

