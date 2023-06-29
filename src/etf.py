import get_data
import configurationFile as config 

class Etf:
    
    def __init__(self, ticker, name):
        self.ticker = ticker # ticker -> 'JNK'
        self.name = name # name -> 'HighYieldBonds'
        self.basecell = config.ETFBASECELL[ticker] # ticker cell in tp -> 'C7' 
        self.colbase = self.basecell[0] # letter of basecell -> 'C' 
        self.rowbase = int(self.basecell[1:]) # row num of basecell -> '7'

        self.indicatorDict = {} # { indicator: value from polygon }
        indicators = get_data.get_indicators(ticker, config.PARAMSET)
        for i in range(len(config.INDICATORS)):
            self.indicatorDict[config.INDICATORS[i]] = indicators[i]
        
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
