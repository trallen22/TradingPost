'''
Main file for auto-populating the Trading Post excel 
'''

# TODO11: Work to auto fill Trading Post Excel (not platform) 

from textwrap import fill
import configuration_file as config
from generate_csv import generate_csv
from tp_helper import fill_excel, generate_tp
import openpyxl

generate_csv()
# fill_excel()
# generate_tp()

# x = openpyxl.load_workbook()