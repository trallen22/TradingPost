'''
This is the main execution. Generates Trading Posts, Platforms and basic csv's

log numbers 100-199
'''

import multiprocessing
from tqdm import tqdm
from etf import Etf 
import configuration_file as config
from generate_files import generate_csv, fill_platform, generate_tp
from send_email import send_email
from simData import run_simulation

multiprocessing.freeze_support() # prevents multithreading in pyinstaller --onedir

etfDict = {} # { str ticker : etf object }

# run a simulation for Trading Post 
if (config.SIMULATE): 
    run_simulation()

exit(0)

# gets tickers and values 
if (config.PBAR):
    pBar = tqdm(desc='tickers found', total=len(config.TICKERS)) # progress bar 
for ticker in config.TICKERS:
    # creates a dictionary of Etf objects { ticker: Etf object }
    etfDict[ticker] = Etf(ticker) 
    if (config.PBAR):
        pBar.update(1)
if (config.PBAR):
    pBar.close()


# generate CSV 
if (config.CSV): 
    if (generate_csv(etfDict, config.CSVFILE)):
        config.logmsg('ERROR', 101, 'unable to generate CSV')
    else:
        config.logmsg('INFO', 102, f'saved csv file to {config.CSVFILE}')

# generate the Trading Post 
if (config.TP):
    if (generate_tp(etfDict, config.OUTPUTEXCEL)):
        config.logmsg('ERROR', 108, 'unable to generate TP')
    else:
        config.logmsg('INFO', 109, f'saved TP file to {config.OUTPUTEXCEL}')

# generate Platform 
if (config.FILLPLATFORM): 
    if (fill_platform(etfDict, config.OUTPUTPLATFORM)):
        config.logmsg('ERROR', 103, 'unable to generate Platform')
    else:
        config.logmsg('INFO', 104, f'saved platform to {config.OUTPUTPLATFORM}')

# send email to email list 
if (config.SENDEMAIL): 
    for address in config.EMAILLIST:
        config.logmsg('DEBUG', 107, f'sending email to \'{address}\'')
        attachments = [config.OUTPUTEXCEL] 
        if (send_email(address, f'Trading Post for {config.STRTODAY}', f'Trading Post for {config.STRTODAY}', attachments)):
            config.logmsg('ERROR', 105, f'unable to send email to \'{address}\'')
        else:
            config.logmsg('INFO', 106, f'successfully sent email to \'{address}\'')
    # for address in config.TestPlatformEMAILLIST:
    #     config.logmsg('DEBUG', 110, f'sending email to \'{address}\'') 
    #     attachments = [config.OUTPUTPLATFORM]
    #     if (send_email(address, 'Todays Trading Post', 'Today\'s Trading Post', attachments)):
    #         config.logmsg('ERROR', 108, f'unable to send email to \'{address}\'')
    #     else:
    #         config.logmsg('INFO', 109, f'successfully sent email to \'{address}\'')