'''
Main file for auto-populating the Trading Post excel 
'''

# TODO11: Work to auto fill Trading Post Excel (not platform) 

from textwrap import fill
import configurationFile as config
from generate_csv import generate_csv
from copyExcel import fill_excel

#generate_csv()
fill_excel()