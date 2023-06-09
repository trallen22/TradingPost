'''
This file holds all the configuraion information
'''
from datetime import date
from polygon import RESTClient 

# convert todays date to mm/dd form 
today = date.today()

listDate = str(today).split('-')
TODAYDATE = f'{listDate[1]}/{listDate[2]}' 

STRTODAY = today.strftime('%Y-%m-%d') # used with polygon data

PRINTDF = 1 # prints dataframes to terminal

# polygon login 
'''Insert your key. Play around with the free tier key first.'''
key = "nGJdIcDOy3hzWwn6X6gritFJkgDWTpRJ"
client = RESTClient(key)
DFPARAM = [[ client, 
                ]]

TEMPLATEEXCELFILE = 'TA.WORK.xlsx'
OUTPUTEXCELFILE = 'testOutputExcel.xlsx'

CSVFILE = 'etf.csv'

TESTCSV = 'etf3.csv'

TICKERS = ["JNK", "GDX", "VCR", "VDC", "VIG", "VDE", "VFH", 
        "VWO", "VHT", "VIS", "VGT", "VAW", "VNQ", "VOO", 
        "VOX", "BND", "BNDX", "VXUS", "VTI", "VPU", "XTN"]

TESTTICKERS = ["JNK"]

INDICATORS = ['one_day_50', 'one_day_200', 'five_min_50', 'five_min_200', 'one_min_50', 'one_min_200']

INPUTS = { 'G':'last_price', 'H':'one_day_50', 'I':'one_day_200', 'J':'five_min_50', 
        'K':'five_min_200', 'L':'one_min_50', 'M':'one_min_200' }