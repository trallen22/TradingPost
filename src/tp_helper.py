'''
This script copies the template excel file from configurationFile.py and 
creates the new excel for current day based on generated csv

log numbers 400-499
'''

import configuration_file as config

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

# TODO19: Implement set_ranges 
def set_ranges(rangeType, etf):
    if rangeType == 'buy':
        rangeMin = buy_min(etf)
        rangeMax = buy_max(etf)
    elif rangeType == 'sell':
        rangeMin = sell_min(etf)
        rangeMax = sell_max(etf)
    else:
        return '', '', 1
    if rangeMin > rangeMax:
        return '', '', 1
    return rangeMin, rangeMax, 0

def determine_buy_sell(etf):
    etfVals = etf.indicatorDict
    signal = None
    color = None
    minTradeRange = None
    maxTradeRange = None 

    if (etfVals['close_price'] > etfVals['one_day_50']):
        # Looking for sell signals 
        if (etfVals['close_price'] > etfVals['one_day_200']):
            minPrice = 1000000000
            for col in config.MINDICATORS:
                minPrice = min(minPrice, etfVals[col])
            if (etfVals['close_price'] < minPrice):
                signal = '!SELL!' 
                color = config.SELLCOLOR
            else:
                signal = 'HOLD' 
                color = config.HOSELLCOLOR
            minTradeRange, maxTradeRange, clearTP = set_ranges('sell', etf)
            if (not clearTP):
                return signal, color, minTradeRange, maxTradeRange
    else:
        # Looking for buy signals 
        if (etfVals['close_price'] < etfVals['one_day_50']):
            maxPrice = -1
            for col in config.MINDICATORS:
                maxPrice = max(maxPrice, etfVals[col])
            if (etfVals['close_price'] > maxPrice):
                signal = '!BUY!' 
                color = config.BUYCOLOR 
            else:
                signal = 'HOLD' 
                color = config.HOBUYCOLOR 
            minTradeRange, maxTradeRange, clearTP = set_ranges('buy', etf)
            if (not clearTP):
                return signal, color, minTradeRange, maxTradeRange
    signal = 'HOLD' 
    color = config.PLAINCOLOR 
    minTradeRange, maxTradeRange, clearTP = set_ranges('', etf)
    return signal, color, minTradeRange, maxTradeRange
