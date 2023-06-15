'''
This file holds all the configuraion information
'''
from datetime import date
from polygon import RESTClient 
import os

SRCPATH = os.path.dirname(__file__) + '/'

# convert todays date to mm/dd form 
today = date.today()

listDate = str(today).split('-')
TODAYDATE = f'{listDate[1]}/{listDate[2]}' 

STRTODAY = today.strftime('%Y-%m-%d') # used with polygon data

PRINTDF = 0 # prints dataframes to terminal
PBAR = 1 # print progress bar for polygon calls in generate_csv.py 

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

# Trading Post variables 
TEMPEXCEL = SRCPATH + 'stocktradingpost2.xlsx'
OUTPUTEXCEL = SRCPATH + 'testTradingPost.xlsx'

CSVFILE = SRCPATH + 'etf.csv' 
# CSVFILE = SRCPATH + 'etf3.csv' # used for testing 

TICKERS = ["JNK", "GDX", "VCR", "VDC", "VIG", "VDE", "VFH", 
        "VWO", "VHT", "VIS", "VGT", "VAW", "VNQ", "VOO", 
        "VOX", "BND", "BNDX", "VXUS", "VTI", "VPU", "XTN"]

# TICKERS = ["JNK"] # used for testing 

INDICATORS = ['one_day_50', 'one_day_200', 'five_min_50', 'five_min_200', 'one_min_50', 'one_min_200', 'close_price']

INPUTS = { 'G':'last_price', 'H':'one_day_50', 'I':'one_day_200', 'J':'five_min_50', 
        'K':'five_min_200', 'L':'one_min_50', 'M':'one_min_200' }

POSTINPUTS = {  }