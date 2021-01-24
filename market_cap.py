import yahoo_fin.stock_info as si
from utils import calculate_pct
from utils import sort_by_date_str

debug = False


# https://stackoverflow.com/questions/11896560/how-can-i-consistently-convert-strings-like-3-71b-and-4m-to-numbers-in-pytho
def text_to_num(text):
    if isinstance(text, float):
        return text
    d = {'M': 6, 'B': 9, 'T': 12}
    if text[-1] in d:
        num, magnitude = text[:-1], text[-1]
        return float(num) * 10**d[magnitude]
    else:
        return float(text)


def fetch_market_cap(ticker):
    stats_valuation = si.get_stats_valuation(ticker)
    series = stats_valuation.loc[stats_valuation.index[0]]
    if debug:
        print(series)
    current_market_cap = 0
    market_cap = {}
    i = 0
    for d in series.index:
        if i > 5:
            break
        i = i + 1
        value = series[d]
        if 'Unnamed' in d:
            if 'Market Cap' not in value:
                print('unexpected ' + value)
                return None
            continue
        if 'As of Date:' in d:
            current_market_cap = value
            market_cap[d[len('As of Date: '):]
                       [:-1 * len('Current')]] = text_to_num(value)
        else:
            market_cap[d] = text_to_num(value)
    if debug:
        print("markey_cap {}".format(market_cap))
    return current_market_cap, market_cap


def quarterly_market_cap_roc(ticker):
    current_market_cap, quarterly_market_caps = fetch_market_cap(ticker)
    sorted_valuations = sort_by_date_str(quarterly_market_caps, '%m/%d/%Y')
    return current_market_cap, calculate_pct(sorted_valuations, ticker)
