import openpyxl 
import configurationFile as config


def buy_min(etf):
    etfVals = etf.indicatorDict
    maxPrice = -1
    for col in config.MINDICATORS:
        maxPrice = max(maxPrice, etfVals[col])
    return maxPrice + 0.01 

def buy_max(etf):
    etfVals = etf.indicatorDict
    dayMin = 100000
    for col in config.DAYDICATORS:
        dayMin = min(dayMin, etfVals[col])
    minuteMax = -1 
    minuteMin = 100000
    for col in config.MINDICATORS:
        minuteMax = max(minuteMax, etfVals[col])
        minuteMin = min(minuteMin, etfVals[col])
    if dayMin > minuteMax:
        return dayMin - 0.01
    else:
        return minuteMin - 0.01

def sell_min(etf):
    etfVals = etf.indicatorDict
    maxVal = -1 
    for col in config.DAYDICATORS:
        maxVal = max(maxVal, etfVals[col])
    return maxVal + 0.01

def sell_max(etf):
    return 2
