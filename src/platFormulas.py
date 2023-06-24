import openpyxl 
import configurationFile as config

def buy_min(etf):
    for interval in config.INDICATORS:
        maxPrice = max()