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
            print("{} {} {}".format(ticker, date, revenues[date]))

    revenues_pct_change = pd.Series(revenues_list).pct_change()
    result = []
    for key in revenues_pct_change.keys():
        if(not pd.isnull(revenues_pct_change[key])):
            result.append(revenues_pct_change[key]*100)

    return result

def process_tickers(tickers):
    df = pd.DataFrame(columns=['Q-3', 'Q-2', 'Q-1'])
    for t in tickers:
        if debug:
            print("Processing {}".format(t))
        df.loc[t] = quarterly_earnings_roc(t)
    return df

tickers = ['four', 'stne']
df = process_tickers(tickers)
print(df)
