import pandas as pd
import yahoo_fin.stock_info as si
from utils import calculate_pct
from utils import sort_by_date
from yahoo_fin import options

debug = False

def quarterly_revenues_roc(ticker):
    revenues = si.get_income_statement(ticker, yearly = False).loc['totalRevenue']
    if debug:
        print(revenues)
    result =  calculate_pct(sort_by_date(revenues), ticker)
    if debug:
        print("{} {}".format(ticker, result))
    return result
