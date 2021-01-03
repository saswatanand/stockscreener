import pandas as pd
from revenue import quarterly_revenues_roc
from market_cap import market_cap_roc

debug = False

def process_tickers(tickers):
    df = pd.DataFrame(columns=['R:Q-3', 'R:Q-2', 'R:Q-1', 'MC:Q-3', 'MC:Q-2', 'MC:Q-1', 'MC:Q-0'])
    for t in tickers:
        if debug:
            print("Processing {}".format(t))
        row = []

        qe_roc = quarterly_revenues_roc(t)
        #print("qe_roc: {}".format(qe_roc))
        for i in range(len(qe_roc), 3):
            row.append(float("NaN"))
        row.extend(qe_roc)
            
        mc_roc = market_cap_roc(t)
        #print("mc_roc: {}".format(mc_roc))
        for i in range(len(mc_roc), 4):
            row.append(float("NaN"))
        row.extend(mc_roc)
            
        if debug:
            print("row {}".format(row))
        df.loc[t] = row
    return df

tickers = ['four', 'stne']
#tickers = ['four']
df = process_tickers(tickers)
print(df)
