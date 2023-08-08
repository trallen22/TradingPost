'''
This file holds all the configuraion information

log numbers 001-099
'''

from datetime import date, timedelta
from polygon import RESTClient 
import os
import sys 
from sys import exit
import openpyxl

# logmsg: logs a given message to the log file at LOGFILE
# parameters: 
#       level - string, log level for message urgency -> 'ERROR', 'INFO', 'NOTICE', 'DEBUG' 
#       logNum - int/string, log ID number for current message
#       message - string, message to log 
# returns:  No returns 
def logmsg(level, logNum, message):
    logMessage = f'{date.today()}::{level}::{logNum}::{message}'
    # prints messages that aren't DEBUG 
    if not (level == 'DEBUG'): 
        print(logMessage)
    try: 
        # writes output to LOGFILE, checks if DEBUG is enabled 
        with open(LOGFILE, mode='a') as logFile:
            if not (level == 'DEBUG' and not DEBUG):
                logFile.write(f'{logMessage}\n')
    except Exception as e:
        print(f'{e}')

PRINTDF = 0 # prints dataframes to terminal
PBAR = 1 # print progress bar for polygon calls in main.py
DEBUG = 0 # log debug messages to LOGFILE 
CSV = 0 # outputs an excel file to CSVFILE 
FILLPLATFORM = 0 # outputs a platform to OUTPUTPLATFORM 
SENDEMAIL = 0 # sends an email to EMAILLIST 
GETVALUE = 0 # gets a specific value from given date 

# TODO: convert todays date to mm/dd form; I don't remember what this means 
today = date.today() # TODO: add command argument to change this 

helpMenu = 'Usage: main.py [-options]\n \
        -h,  Opens this help menu\n \
        -f,  Print dataframes to the terminal\n \
        -p,  Show progress bar\n \
        -d,  logs Debug messages to LOGFILE\n \
        -c,  Generate a CSV file with ticker data\n \
        -m,  Generate a Platform file with ticker data\n \
        -g,  Geneartes CSV and Platform files\n \
        -e,  Send email to addresses in email list\n \
        -v,  Get specific value by date, interval and ticker\n'

for arg in sys.argv[1:]: # skip main.py
    if arg == '-h':
        print(helpMenu)
        exit(0)
    elif arg == '-f':
        PRINTDF = 1
    elif arg == '-p':
        PBAR = 1 
    elif arg == '-d':
        DEBUG = 1 
    elif arg == '-c':
        CSV = 1
    elif arg == '-m':
        FILLPLATFORM = 1 
    elif arg == '-e':
        SENDEMAIL = 1
    elif arg == '-v':
        GETVALUE = 1
    elif arg == '-g':
        CSV = 1
        FILLPLATFORM = 1
    elif arg == '-t':
        index = sys.argv.index('-t')

    else:
        print(f'NOTICE::003::bad argument given \'{arg}\'')
        # logmsg('NOTICE', '003', f'bad argument given \'{arg}\'')

listDate = str(today).split('-')
TODAYDATE = f'{listDate[1]}/{listDate[2]}'  # mm/yy

STRTODAY = today.strftime('%Y-%m-%d') # used with polygon data; yy-mm-dd

# Email variables 
EMAILADDRESS = 'etfsender@gmail.com'
EMAILPASSWORD = 'egztwpmmkbicpjfd' # 'P@55w0rd123' 
EMAILLIST = [ 'trallen@davidson.edu', 'michaelgkelly01@yahoo.com', 'ludurkin@davidson.edu', 'hannachrisj@gmail.com' ] 
# EMAILLIST = [ 'trallen@davidson.edu' ] # can be used for testing 

# determine if application is a script file or frozen exe
# not sure what this means, found it on stack overflow 
if getattr(sys, 'frozen', False):
    curDir = os.path.dirname(sys.executable)
elif __file__:
    curDir = os.path.abspath(__file__)

dirList = curDir.split('/')
dirIndex = dirList.index('TradingPost')
topList = dirList[:dirIndex+1]

TPROOT = '/'.join(topList) # root directory for trading post execution 

# Debug files 
LOGROOT = f'{TPROOT}/debug'
LOGFILE = f'{LOGROOT}/logfile.txt'
try:
    os.mkdir(f'{LOGROOT}')
    logmsg('DEBUG', '008', f'created src directory \'{LOGROOT}\'')
except FileExistsError:
    with open(LOGFILE, mode='r+') as lf:
        lastLines = lf.readlines()[-100:]
    with open(LOGFILE, mode='w') as lf:
        for line in lastLines:
            lf.write(line)
    logmsg('DEBUG', '009', f'debug directory already created at \'{LOGROOT}\'')

# Template files 
SRCROOT = f'{TPROOT}/src'
TEMPLATEPLATFORM = f'{SRCROOT}/TA.WORK.xlsx' 
TEMPEXCEL = f'{SRCROOT}/stocktradingpost.xlsx' 
try:
    os.mkdir(f'{SRCROOT}')
    logmsg('DEBUG', '004', f'created src directory \'{SRCROOT}\'')
except FileExistsError:
    logmsg('DEBUG', '005', f'src directory already created at \'{SRCROOT}\'')

# Output files 
OUTROOT = f'{TPROOT}/testTP'
OUTPUTPLATFORM = f'{OUTROOT}/{listDate[1]}-{listDate[2]}_testPlatform.xlsx'
OUTPUTEXCEL = f'{OUTROOT}/{listDate[1]}-{listDate[2]}_testTradingPost.xlsx'
CSVFILE = f'{OUTROOT}/{listDate[1]}-{listDate[2]}_csv.csv' 
try:
    os.mkdir(f'{OUTROOT}')
    logmsg('DEBUG', '006', f'created src directory \'{OUTROOT}\'')
except FileExistsError:
    logmsg('DEBUG', '007', f'output directory already created at \'{OUTROOT}\'')

# polygon login 
key = "CP1nN_q8W8C4eG7phIPNgLNCyPEyDZPe" # paid standard version 
try:
    CLIENT = RESTClient(key)
    logmsg('DEBUG', '001', 'loading RESTClient')
except Exception as e:
    logmsg('ERROR', '002', f'{e}')

TICKERS = [ 'JNK', 'GDX', 'VCR', 'VDC', 'VIG', 'VDE', 'VFH', 
        'VWO', 'VHT', 'VIS', 'VGT', 'VAW', 'VNQ', 'VOO', 
        'VOX', 'BND', 'BNDX', 'VXUS', 'VTI', 'VPU', 'XTN' ]

# TICKERS = [ 'JNK' ] # used for testing 

PARAMSET = [[ 'minute', 1 ], # one minute time interval 
            [ 'minute', 5 ], # 5 minute time interval 
            [ 'day', 1 ]] #one day time interval 

INDICATORS = [ 'one_min_50', 'one_min_200', 'five_min_50', 'five_min_200', 'one_day_50', 'one_day_200', 'close_price' ]
MINDICATORS = [ 'five_min_50', 'five_min_200', 'one_min_50', 'one_min_200' ]
DAYDICATORS = [ 'one_day_50', 'one_day_200' ]

# this is { platform column: indicator }
INPUTS = { 'G':'close_price', 'H':'one_day_50', 'I':'one_day_200', 'J':'five_min_50', 
            'K':'five_min_200', 'L':'one_min_50', 'M':'one_min_200' }

PLATFORMCOLS = { 'date':'E', 'close_price':'G', 'one_day_50':'H', 'one_day_200':'I', 'five_min_50':'J', 
            'five_min_200':'K', 'one_min_50':'L', 'one_min_200':'M' }

# base cell for each ticker in Trading Post excel 
ETFBASECELL = { 'JNK':'C7', 'GDX':'D7', 'VCR':'E7', 'VDC':'F7', 'VIG':'G7', 
            'VDE':'H7', 'VFH':'I7', 'VWO':'C17', 'VHT':'D17', 'VIS':'E17', 'VGT':'F17', 
            'VAW':'G17', 'VNQ':'H17', 'VOO':'I17', 'VOX':'C27', 'BND':'D27', 
            'BNDX':'E27', 'VXUS':'F27', 'VTI':'G27', 'VPU':'H27', 'XTN':'I27' }

# cell with date in Trading Post 
PLATDATECELL = 'B3'

try: 
    # loading excel as workbook object
    workbook = openpyxl.load_workbook(TEMPEXCEL)
    excelSheet = workbook.active
except Exception as e:
    print(f'ERROR: {e}')
    exit(4)

COLORROW = 5 # row on trading post excel with template color
plainRGB = 'FFFFFFFF' # color white 
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
