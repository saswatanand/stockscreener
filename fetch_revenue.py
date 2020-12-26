import pandas as pd
import yahoo_fin.stock_info as si

from yahoo_fin import options

debug = False

def quarterly_earnings_roc(ticker):
    revenues = si.get_income_statement(ticker, yearly = False).loc['totalRevenue']
    revenues_list = []
    for date in sorted(revenues.keys(), ):
        revenues_list.append(revenues[date])
        if debug:
            print("{} {}".format(date, revenues[date]))

    revenues_pct_change = pd.Series(revenues_list).pct_change()
    result = []
    for key in revenues_pct_change.keys():
        if(not pd.isnull(revenues_pct_change[key])):
            result.append(revenues_pct_change[key]*100)

    return result

tickers = ['four', 'stne']
for t in tickers:
    print(t)
    print(quarterly_earnings_roc(t))
