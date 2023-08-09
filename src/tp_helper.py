'''
This script copies the template excel file from configurationFile.py and 
creates the new excel for current day based on generated csv

log numbers 400-499
'''

import configuration_file as config

# buy_min: determines the buy range minimum value. Helper function 
#           for set_ranges.  
# parameters: 
#       etf - Etf object, current etf to get range for 
# returns: integer, the buy range minimum value 
def buy_min(etf):
    etfVals = etf.indicatorDict
    maxPrice = -1
    for col in config.MINDICATORS:
        maxPrice = max(maxPrice, etfVals[col])
    return maxPrice + 0.01 

# buy_max: determines the buy range maximum value. Helper function 
#           for set_ranges.  
# parameters: 
#       etf - Etf object, current etf to get range for 
# returns: integer, the buy range maximum value 
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

# sell_min: determines the sell range minimum value. Helper function 
#           for set_ranges.  
# parameters: 
#       etf - Etf object, current etf to get range for 
# returns: integer, the sell range minimum value 
def sell_min(etf):
    etfVals = etf.indicatorDict
    maxVal = -1 
    for col in config.DAYDICATORS:
        maxVal = max(maxVal, etfVals[col])
    return maxVal + 0.01

# sell_max: determines the sell range maximum value. Helper function 
#           for set_ranges. 
# parameters: 
#       etf - Etf object, current etf to get range for 
# returns: integer, the sell range maximum value 
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

# set_ranges: determines the trade ranges in the Trading Post excel 
# parameters: 
#       etf - Etf object, current etf to get range for 
# returns: returns the current ranges minimum, maximum and 
#           if the cells should be cleared 
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

# determine_buy_sell: determines the Buy, Sell, or Hold signal for a given etf 
# parameters: 
#       etf - Etf object, current etf to determine signal for  
# returns: 
#       signal - string, BUY/SELL/HOLD signal 
#       color - color (not sure class or type), cell color for determined signal 
#       minTradeRange - integer/string, minimum value for current etf trade range 
#       maxTradeRange - integer/string, maximum value for current etf trade range 
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
    # if it can't choose a Buy or Sell signal, chooses Hold 
    signal = 'HOLD' 
    color = config.PLAINCOLOR 
    minTradeRange, maxTradeRange, clearTP = set_ranges('', etf)
    return signal, color, minTradeRange, maxTradeRange
