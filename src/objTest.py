from etf import Etf 
import configurationFile as config

x = Etf(config.TICKERS[0], 'name')

for i in range(len(config.INDICATORS)):
    print(x.indicatorDict[config.INDICATORS[i]])