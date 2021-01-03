import pandas as pd
import yahoo_fin.stock_info as si
from yahoo_fin import options
from utils import calculate_pct
from utils import sort_by_date_str

debug = False

# https://stackoverflow.com/questions/11896560/how-can-i-consistently-convert-strings-like-3-71b-and-4m-to-numbers-in-pytho
def text_to_num(text):
    d = {'M': 6, 'B': 9}
    if text[-1] in d:
        num, magnitude = text[:-1], text[-1]
        return float(num) * 10 ** d[magnitude]
    else:
        return float(text)

def fetch_market_cap(ticker):
    df = si.get_stats_valuation(ticker)
    series = df.loc[df.index[0]]
    if debug:
        print(series)
    market_cap = {}
    i = 0
    for d in series.index:
        if i > 5:
            break
        i = i + 1
        value = series[d]
        if 'Unnamed' in d:
            if 'Market Cap' not in value:
                print('unexpected '+value)
                return None
            continue
        if 'As of Date:' in d:
            market_cap[d[len('As of Date: '):][:-1*len('Current')]] = text_to_num(value)
        else:
            market_cap[d] = text_to_num(value)
    if debug:
        print("markey_cap {}".format(market_cap))
    return market_cap

def market_cap_roc(ticker):
    valuation = fetch_market_cap(ticker)
    return calculate_pct(sort_by_date_str(valuation, '%m/%d/%Y'), ticker)
        
