'''
This might not work or be necessary
'''

# from _typeshed import NoneType
# import yfinance as yf
from bs4 import BeautifulSoup
import requests
from pprint import pprint
# import pandas as pd

cookies = {
    'NID': '511=jFZdNhh9JLaLTn2OfLnv9s-Ms88khwcauSa-hvokWdzzAnT0sx_iYaKHPmwUjaubmGIRYvGK01mNv-KWyPUat8jpJ6Jb8rYKZLeTnLzrdQMNLIEeoq67BZSQ4-nEsPyYNfu-qAKexZOAuuADvfDfOxFsOFnWR6My3xu3EDpQCdBa__WsSGOzPmjuj7vpAwSZTd9DBAaGG3K0hK0RKQ7msw6aPTWOuQ9b_ugixmvtZ___lF8H7E84nHZ9tkB5vWFWlDsKX_YjyrTiY6opSCox719jRPBTwpsdrlcWuIXU29koMJ8v4bUunZ8kn9yaECe6GwOSIOLN9IcufitustyNiJDnU_-KmB-6I2TLwFLi7qKRQCSzzsEhDPD96Cpvv5AL2JbesQh3SKA7jgEx0khe-zZWbcJ6iquJedE',
    'SID': 'UQgDhqhFCNmnWUzQLRdwFqYxx6Tlsa54e8wx4Q6aMHOV_ULgxsbgvQ7iXstdFxYBOrgN9g.',
    'HSID': 'ATXrzkoBuvB-vAsv0',
    'SSID': 'AE9YE-69iGGayhPiy',
    'APISID': '_ZHnUSzXj-r4ZlgG/AHJSut1e61w-2xGoY',
    'SAPISID': 'ugaIgn0m1NXqrdFE/AydNamXeDsXKwb6td',
    'SIDCC': 'AFvIBn8mIzmOzOPAr-bIp4uvyVWB6rb-gYTskY90XrXCpZ2hbM0PRMYVoWIJ94DSgkneYlEIznE',
    '__Secure-3PSID': 'UQgDhqhFCNmnWUzQLRdwFqYxx6Tlsa54e8wx4Q6aMHOV_ULgbdtDVmHCrjSOTfzmQnr4MQ.',
    '__Secure-3PAPISID': 'ugaIgn0m1NXqrdFE/AydNamXeDsXKwb6td',
    '__Secure-3PSIDCC': 'AFvIBn_biLaqj1zwthgnQy-TgOPchpn3eobTY2aZtMbzBe4HGPoOqSY0WQD-88unkOq6DSLYsqk',
    '__Secure-1PSID': 'UQgDhqhFCNmnWUzQLRdwFqYxx6Tlsa54e8wx4Q6aMHOV_ULgy93PJxibB0IHQhbyjDcjpA.',
    '__Secure-1PAPISID': 'ugaIgn0m1NXqrdFE/AydNamXeDsXKwb6td',
    '__Secure-1PSIDCC': 'AFvIBn82BQnRrVwsBGgqFhFD5kcKrckkeWggoUkS7UnHr37uBaESAK26n89xpCfB-2sc8X45Kkc',
    '1P_JAR': '2023-3-23-1',
    'ANID': 'AHWqTUmVOVQpyDguopBSFrrtzv45lOmjWv6WrXNvAezl_XSsyMAHwtHsjW0rBAf8',
    'OTZ': '6940445_72_76_104100_72_446760',
    'AEC': 'ARSKqsI_nYL0DWf5yI0igUtscaJsUwX_GpQnUJ1Xhh1V6sycRFJs7t7D8VQ',
    'DV': 'U5cIt8E_piYR8DWt3o2g3zLT9T3BcBg',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    # 'Cookie': 'NID=511=jFZdNhh9JLaLTn2OfLnv9s-Ms88khwcauSa-hvokWdzzAnT0sx_iYaKHPmwUjaubmGIRYvGK01mNv-KWyPUat8jpJ6Jb8rYKZLeTnLzrdQMNLIEeoq67BZSQ4-nEsPyYNfu-qAKexZOAuuADvfDfOxFsOFnWR6My3xu3EDpQCdBa__WsSGOzPmjuj7vpAwSZTd9DBAaGG3K0hK0RKQ7msw6aPTWOuQ9b_ugixmvtZ___lF8H7E84nHZ9tkB5vWFWlDsKX_YjyrTiY6opSCox719jRPBTwpsdrlcWuIXU29koMJ8v4bUunZ8kn9yaECe6GwOSIOLN9IcufitustyNiJDnU_-KmB-6I2TLwFLi7qKRQCSzzsEhDPD96Cpvv5AL2JbesQh3SKA7jgEx0khe-zZWbcJ6iquJedE; SID=UQgDhqhFCNmnWUzQLRdwFqYxx6Tlsa54e8wx4Q6aMHOV_ULgxsbgvQ7iXstdFxYBOrgN9g.; HSID=ATXrzkoBuvB-vAsv0; SSID=AE9YE-69iGGayhPiy; APISID=_ZHnUSzXj-r4ZlgG/AHJSut1e61w-2xGoY; SAPISID=ugaIgn0m1NXqrdFE/AydNamXeDsXKwb6td; SIDCC=AFvIBn8mIzmOzOPAr-bIp4uvyVWB6rb-gYTskY90XrXCpZ2hbM0PRMYVoWIJ94DSgkneYlEIznE; __Secure-3PSID=UQgDhqhFCNmnWUzQLRdwFqYxx6Tlsa54e8wx4Q6aMHOV_ULgbdtDVmHCrjSOTfzmQnr4MQ.; __Secure-3PAPISID=ugaIgn0m1NXqrdFE/AydNamXeDsXKwb6td; __Secure-3PSIDCC=AFvIBn_biLaqj1zwthgnQy-TgOPchpn3eobTY2aZtMbzBe4HGPoOqSY0WQD-88unkOq6DSLYsqk; __Secure-1PSID=UQgDhqhFCNmnWUzQLRdwFqYxx6Tlsa54e8wx4Q6aMHOV_ULgy93PJxibB0IHQhbyjDcjpA.; __Secure-1PAPISID=ugaIgn0m1NXqrdFE/AydNamXeDsXKwb6td; __Secure-1PSIDCC=AFvIBn82BQnRrVwsBGgqFhFD5kcKrckkeWggoUkS7UnHr37uBaESAK26n89xpCfB-2sc8X45Kkc; 1P_JAR=2023-3-23-1; ANID=AHWqTUmVOVQpyDguopBSFrrtzv45lOmjWv6WrXNvAezl_XSsyMAHwtHsjW0rBAf8; OTZ=6940445_72_76_104100_72_446760; AEC=ARSKqsI_nYL0DWf5yI0igUtscaJsUwX_GpQnUJ1Xhh1V6sycRFJs7t7D8VQ; DV=U5cIt8E_piYR8DWt3o2g3zLT9T3BcBg',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

params = {
    'client': 'firefox-b-1-d',
    'q': 'JNK current price',
}

response = requests.get('https://www.google.com/search', params=params, cookies=cookies, headers=headers)

tickers = ["JNK", "GDX", "VCR", "VDC", "VIG", "VDE", "VFH", 
        "VWO", "VHT", "VIS", "VGT", "VAW", "VNQ", "VOO", 
        "VOX", "BND", "BNDX", "VXUS", "VTI", "VPU", "XTN"]

ticker_price = {}    

for ticker in tickers:
        #   'https://www.google.com/search?client=firefox-b-1-d&q=JNK+current+price'
    url = "https://www.google.com/search?client=firefox-b-1-d&q=" + ticker + "+current+price"
    # print(url)
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')
    # <span jsname="vWLAgc" class="IsqQVc NprOob wT3VGc">90.79</span>
    # articles = soup.find("span", {"class": "IsqQVc NprOob XcVN5d"})
    articles = soup.find("span", {"class": "IsqQVc NprOob wT3VGc"})
    # pprint(articles)
    # if articles.text != None:
    #     ticker_price[ticker] = articles.text
    # else:
    #     print(ticker + " not found")

pprint(ticker_price)
# response = requests.get('https://www.google.com/search?client=firefox-b-1-d&q=VIG+current+price', headers=headers, cookies=cookies)


# soup = BeautifulSoup(response.content, 'html.parser')

# articles = soup.find("span", {"class": "IsqQVc NprOob XcVN5d"})

# print(articles.text)

# import investpy

# df = investpy.get_stock_historical_data(stock='msft',
#                                         country='United States',
#                                         from_date='11/11/2021',
#                                         to_date='11/12/2021')
# print(df.head())



# msft = yf.Ticker("MSFT")

# # 'fiftyDayAverage'
# # 'twoHundredDayAverage'

# fiftydayavg = msft.info['fiftyDayAverage']
# twohundayavg = msft.info['twoHundredDayAverage']
# curr_price = msft.info['currentPrice']

# print("Current Price: " + str(curr_price))

# ticker_price = {}

# for ticker in tickers:
#     curr = yf.Ticker(ticker)
#     print(ticker)
#     try:
#         ticker_price[ticker] = yf.Ticker(ticker).info['currentPrice']
#     except:
#         print(ticker + " not found")

# pprint(ticker_price)

# msft = yf.Ticker("MSFT")

# # 'fiftyDayAverage'
# # 'twoHundredDayAverage'

# fiftydayavg = msft.info['fiftyDayAverage']
# twohundayavg = msft.info['twoHundredDayAverage']
# curr_price = msft.info['currentPrice']

# print("Current Price: " + str(curr_price))
# print("50 day avg: " + str(fiftydayavg))
# print("200 day avg: " + str(twohundayavg))

# get stock info
# print(msft.info.keys())