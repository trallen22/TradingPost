import polygon_data
import configurationFile as config 

class Etf:
    
    def __init__(self, ticker, name):
        self.ticker = ticker # ticker -> 'JNK'
        self.name = name # name -> 'HighYieldBonds'
        self.basecell = config.ETFBASECELL[ticker] # ticker cell in tp -> 'C7' 
        self.colbase = self.basecell[0] # letter of basecell -> 'C' 
        self.rowbase = int(self.basecell[1:]) # row num of basecell -> '7'

        self.indicatorDict = {} # { indicator: value from polygon }
        indicators = polygon_data.get_indicators(ticker, config.PARAMSET)
        for i in range(len(config.INDICATORS)):
            self.indicatorDict[config.INDICATORS[i]] = indicators[i]
        
