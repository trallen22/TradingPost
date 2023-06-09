from polygon import RESTClient
from datetime import datetime, timedelta
import pandas as pd 
import numpy as np

'''This file is for debugging'''

ticker = "VOO"

'''Insert your key. Play around with the free tier key first.'''
key = ""
client = RESTClient(key)

to = datetime.today() - timedelta(1) 
days = timedelta(7)
from_ = datetime.today() - timedelta(1) 

to += timedelta(seconds=0, minutes=39, hours=15)
from_ += timedelta(seconds=0, minutes=35, hours=14)

# to = to.strftime('%Y-%m-%d')

# print(to)
# from_ = from_.strftime('%Y-%m-%d')

resp = client.get_aggs(ticker=ticker, multiplier=1, timespan = "minute", from_=from_, to=to, adjusted=True, sort="desc")
df = pd.DataFrame(resp)

print(df.head(5))