from openpyxl import Workbook
from openpyxl import load_workbook
from barchart_scrape import get_one_day_avgs
from newpoly import get_minute_indicator
from datetime import datetime, timedelta


# def ts_to_datetime(ts) -> str:
#     return datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')

# def ts_to_hour(ts) -> int:
#     return int(datetime.fromtimestamp(ts / 1000.0).hour)

# def ts_to_min(ts) -> int:
#     return int(datetime.fromtimestamp(ts / 1000.0).minute)

# def ts_to_time_of_day(ts) -> timedelta:
#     return timedelta(seconds=ts.second,minutes=ts.minute,hours=ts.hour)

to = datetime.today()
days = timedelta(7)
from_ = to - days
to = to.strftime('%Y-%m-%d')
from_ = from_.strftime('%Y-%m-%d')

####### Need to figure out how to write file name as an F string so each overwrite
####### has updated date for range of inormation

full_time = f"{from_} to {to}"


tickers = ["JNK", "GDX", "VCR", "VDC", "VIG", "VDE", "VFH", 
        "VWO", "VHT", "VIS", "VGT", "VAW", "VNQ", "VOO", 
        "VOX", "BND", "BNDX", "VXUS", "VTI", "VPU", "XTN"]

smalltickers = ["JNK"]

# print(tickers,"\n")

one_day_fifty, one_day_two_hundred = get_one_day_avgs(smalltickers)

one_minute_fifty, one_minute_two_hundred, five_minute_fifty, five_minute_two_hundred = get_minute_indicator(smalltickers)

######IGNORE#####
# one_minute_fifty, one_minute_two_hundred, five_minute_fifty, five_minute_two_hundred, last_price = get_minute_indicator(tickers)

####FIX#####

wb = Workbook()
ws = wb.active

columnnames = ['ticker', 'one_day_50', 'one_day_200',
                'five_min_50', 'five_min_200',
                'one_min_50', 'one_min_200',
                'last_price']

ws.append(columnnames)

# with open('etf2.csv', mode='w') as csv_file:
#     fieldnames = ['ticker', 'one_day_50', 'one_day_200',
#                 'five_min_50', 'five_min_200',
#                 'one_min_50', 'one_min_200',
#                 'last_price']
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     writer.writeheader()
try:

    for ticker in one_day_fifty:
        try:
            ws.append({
                'ticker': ticker,
                'one_day_50': one_day_fifty[ticker],
                'one_day_200': one_day_two_hundred[ticker],
                'five_min_50': five_minute_fifty[ticker],
                'five_min_200': five_minute_two_hundred[ticker],
                'one_min_50': one_minute_fifty[ticker],
                'one_min_200': one_minute_two_hundred[ticker],
                # 'last_price': last_price[ticker]
                # 'last_price': last_price[ticker]
            })
        except Exception as e:
            print(f"Error occurred for ticker {ticker}: {e}")
            continue

    wb.save("test.xlsx")
except Exception as e:
    print(f"Error occurred while writing to Excel file: {e}")



