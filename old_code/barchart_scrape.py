from bs4 import BeautifulSoup
from pprint import pprint
import requests



'''
get_one_day_avgs - This function scrapes barchart.com 
                for one day averages for the given ticker. 
parameters: 
    tickers - String, ticker to find the one day averages of 
returns: 
    ticker_fifty - 
'''
def get_one_day_avgs(tickers):
    cookies = {
        'bcFreeUserPageView': '0',
        'laravel_token': 'eyJpdiI6Im0rVmpkMll0NkYvaHZmZUFrcEpaamc9PSIsInZhbHVlIjoiSEZlRW9uVFFoRCt4aGJlOE93SkhCUWdqOHRuWVZvclRsWEl6NzJxOU54WTBYMktDNndmM3g4V0FTd0svTkhTanRmWTVTVUs4T0pWejJLRkd6WHdSUVgrTGlUV3RIa2FOY2o5TFh1ODhzZkhSUEEzUmU0MzUzMXJ0ZHlsSzZjc1JLbW45elJUUVl1cWRKVHhyK2lPSGF1cDBDT2VnMSt4RGlRRkZVRE0vZGlQMnlERmQxeXExaHgxUlNQWDRBaDI4aTJ0cHMwdXdqWldFTmFyYitybWdqd3lkRnZxVjQ4VFlmNGdZUVk4ajhVQURMelFKRGo5T1VIUWRXYVNlczFHV0V2T09CdURIN1F4TENkMkxmbzk5djJ5K01vbEJob2ZXL3pBSkZZT29XZGVWSExFZmRVUndjcUpUaXNsSWgvZzAiLCJtYWMiOiJiY2I0MGYzNjNjZDU2MGY5ZGJkOTRhMzJmNjYyOGUyYmExZjU1NGRkMzMzMWZjYjBiYTRmNzc4YjBhMzcwNDg2In0%3D',
        'XSRF-TOKEN': 'eyJpdiI6IlR3STRENHZhYTlmVFdMcTdOK3JKeVE9PSIsInZhbHVlIjoiNG9IOFdmb2JVa1Y0RDk2M0w2b0k0alJkTmk4MEZXSSt6aEluSzlva0NJYnkrNnp6SmpyVmcrMkQ4WVdLSUs1MkpSalJKb01heXdyZDdXZ09CTzhBM2lCeTY2b0Ntc0IvdjhHOWthMTNLak45VTcwUFZWK2V2OGFhL3FRakZhb0EiLCJtYWMiOiIwODg4NWUyNGZiZmNlOTVlYzdmNDVhNjE5YzgwY2JhMzU0MGQ1NjU0NDJkOTI1MDJlNTg5ZTAyNDZkNjYyOThiIn0%3D',
        'laravel_session': 'eyJpdiI6InI0NVNmTlFaOHIxZjdMNzZmcmtUMlE9PSIsInZhbHVlIjoiTlZkMkFOWHRBWGgxam9HcGRzWnI2MkF5QkhPNEs2M1JZVS84VHp1Qzc2alIvRU9EWFptVVRoYkFkbWVoT3k2QW13eG1SZnJEVHBoMm1uYXk0cUVVdWZ3M25EcFE3d2pWa2h1Tk92dWZZRWpYT1dFQWhqN1I0NjhCSTZvcS9rVlAiLCJtYWMiOiIwOGQ1MTM3NjBkNjJhMDkwYzQ4YjYzYjY4YjA0ZDlkMmY2MjgzOGI3ZjA2YzY3ZDNmMTJmYjhmNTQ3ZmM2ZDE1In0%3D',
        'market': 'eyJpdiI6InA3SkJNamdFdmRKMk1hUWJrem8yZGc9PSIsInZhbHVlIjoiZFBIeHlLcUJoYW1Va1lING9Lc1JKb1NxcHllOEdmRXNRUTJHT0FXWXorelMrNGkxMlJiOUI1bFRyaFZXOXh1WSIsIm1hYyI6ImNjZGRiZWFmOTc2YTRhMjRiMjMwYzg3ZmZhMDEyMTY1OGQwODJkOGM4MTAzYzc1YzBkYWU0MWYwMDAxZDZjZmQifQ%3D%3D',
        'webinar140WebinarClosed': 'true',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.barchart.com/etfs-funds/quotes/SPY/overview',
        'Connection': 'keep-alive',
        # 'Cookie': 'bcFreeUserPageView=0; laravel_token=eyJpdiI6Im0rVmpkMll0NkYvaHZmZUFrcEpaamc9PSIsInZhbHVlIjoiSEZlRW9uVFFoRCt4aGJlOE93SkhCUWdqOHRuWVZvclRsWEl6NzJxOU54WTBYMktDNndmM3g4V0FTd0svTkhTanRmWTVTVUs4T0pWejJLRkd6WHdSUVgrTGlUV3RIa2FOY2o5TFh1ODhzZkhSUEEzUmU0MzUzMXJ0ZHlsSzZjc1JLbW45elJUUVl1cWRKVHhyK2lPSGF1cDBDT2VnMSt4RGlRRkZVRE0vZGlQMnlERmQxeXExaHgxUlNQWDRBaDI4aTJ0cHMwdXdqWldFTmFyYitybWdqd3lkRnZxVjQ4VFlmNGdZUVk4ajhVQURMelFKRGo5T1VIUWRXYVNlczFHV0V2T09CdURIN1F4TENkMkxmbzk5djJ5K01vbEJob2ZXL3pBSkZZT29XZGVWSExFZmRVUndjcUpUaXNsSWgvZzAiLCJtYWMiOiJiY2I0MGYzNjNjZDU2MGY5ZGJkOTRhMzJmNjYyOGUyYmExZjU1NGRkMzMzMWZjYjBiYTRmNzc4YjBhMzcwNDg2In0%3D; XSRF-TOKEN=eyJpdiI6IlR3STRENHZhYTlmVFdMcTdOK3JKeVE9PSIsInZhbHVlIjoiNG9IOFdmb2JVa1Y0RDk2M0w2b0k0alJkTmk4MEZXSSt6aEluSzlva0NJYnkrNnp6SmpyVmcrMkQ4WVdLSUs1MkpSalJKb01heXdyZDdXZ09CTzhBM2lCeTY2b0Ntc0IvdjhHOWthMTNLak45VTcwUFZWK2V2OGFhL3FRakZhb0EiLCJtYWMiOiIwODg4NWUyNGZiZmNlOTVlYzdmNDVhNjE5YzgwY2JhMzU0MGQ1NjU0NDJkOTI1MDJlNTg5ZTAyNDZkNjYyOThiIn0%3D; laravel_session=eyJpdiI6InI0NVNmTlFaOHIxZjdMNzZmcmtUMlE9PSIsInZhbHVlIjoiTlZkMkFOWHRBWGgxam9HcGRzWnI2MkF5QkhPNEs2M1JZVS84VHp1Qzc2alIvRU9EWFptVVRoYkFkbWVoT3k2QW13eG1SZnJEVHBoMm1uYXk0cUVVdWZ3M25EcFE3d2pWa2h1Tk92dWZZRWpYT1dFQWhqN1I0NjhCSTZvcS9rVlAiLCJtYWMiOiIwOGQ1MTM3NjBkNjJhMDkwYzQ4YjYzYjY4YjA0ZDlkMmY2MjgzOGI3ZjA2YzY3ZDNmMTJmYjhmNTQ3ZmM2ZDE1In0%3D; market=eyJpdiI6InA3SkJNamdFdmRKMk1hUWJrem8yZGc9PSIsInZhbHVlIjoiZFBIeHlLcUJoYW1Va1lING9Lc1JKb1NxcHllOEdmRXNRUTJHT0FXWXorelMrNGkxMlJiOUI1bFRyaFZXOXh1WSIsIm1hYyI6ImNjZGRiZWFmOTc2YTRhMjRiMjMwYzg3ZmZhMDEyMTY1OGQwODJkOGM4MTAzYzc1YzBkYWU0MWYwMDAxZDZjZmQifQ%3D%3D; webinar140WebinarClosed=true',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    response = requests.get('https://www.barchart.com/etfs-funds/quotes/SPY/technical-analysis', cookies=cookies, headers=headers)

    ticker_fifty = {}    
    ticker_two_hundred = {}

    for ticker in tickers:
        url = "https://www.barchart.com/etfs-funds/quotes/" + ticker + "/technical-analysis"
        response = requests.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.findAll("td")
        # titles = soup.findAll("th")
        # info[ticker] = articles
        # pprint(ticker)
        # pprint(articles)
        # pprint(articles[0].text)
        # pprint(articles[1].text)
        # pprint(articles[2].text)
        # pprint(articles[3].text)
        # pprint("SPACE/n")
        # pprint(titles)
        # pprint("SPACE/n")
        
        try: 
            fifty_day_avg = articles[11].text
            two_hundred_day_avg = articles[21].text
        except:
            fifty_day_avg = -1
            two_hundred_day_avg = -1

        ticker_fifty[ticker] = fifty_day_avg
        ticker_two_hundred[ticker] = two_hundred_day_avg
        
    return ticker_fifty, ticker_two_hundred


print(get_one_day_avgs(['JNK']))