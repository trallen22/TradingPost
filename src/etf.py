'''
This is the Etf object class module. 

log numbers 180-199
'''

import get_data
import configuration_file as config 
import datetime

class Etf:
    
    # __init__: creates etf object 
    # parameters: 
    #       ticker - string, etf ticker -> 'JNK' 
    #       name - string, etf name -> 'High Yield Bonds' 
    # returns:  no return 
    def __init__(self, ticker, name):
        config.logmsg('DEBUG', 180, f'started creating etf object for \'{ticker}\'')
        self.ticker = ticker # ticker -> 'JNK'
        self.name = name # name -> 'HighYieldBonds'
        self.basecell = config.ETFBASECELL[ticker] # ticker cell in tp -> 'C7' 
        self.colbase = self.basecell[0] # letter of basecell -> 'C' 
        self.rowbase = int(self.basecell[1:]) # row num of basecell -> '7'
        self.indicatorDict = {} # { indicator: value from polygon }
        self.date = config.TODAYDATE

        config.logmsg('DEBUG', 181, f'getting indicators for ticker \'{ticker}\'')
        indicators = get_data.get_indicators(ticker) 

        for i in range(len(config.INDICATORS)):
            self.indicatorDict[config.INDICATORS[i]] = indicators[i]
        config.logmsg('DEBUG', 182, f'done creating etf object for \'{ticker}\'')
        
    def __str__(self):
        return { 'ticker':self.ticker, 
                'name':self.name,
                'tp base cell':self.basecell,
                'close_price':self.indicatorDict['close_price'],
                'one_min_50':self.indicatorDict['one_min_50'], 
                'one_min_200':self.indicatorDict['one_min_200'], 
                'five_min_50':self.indicatorDict['five_min_50'], 
                'five_min_200':self.indicatorDict['five_min_200'], 
                'one_day_50':self.indicatorDict['one_day'], 
                'one_day_200':self.indicatorDict['one_day_200'] }
