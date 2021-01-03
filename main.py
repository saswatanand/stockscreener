import pandas as pd
from revenue import quarterly_revenues_roc
from market_cap import quarterly_market_cap_roc

debug = False

def process_tickers(tickers):
    df = pd.DataFrame(columns=['R:Q-3', 'R:Q-2', 'R:Q-1', 'MC:Q-3', 'MC:Q-2', 'MC:Q-1', 'MC:Q-0', 'MC:current'])
    df.index.name='ticker'
    for t in tickers:
        print("Processing {}".format(t))
        row = []

        qe_roc = quarterly_revenues_roc(t)
        #print("qe_roc: {}".format(qe_roc))
        for i in range(len(qe_roc), 3):
            row.append(float("NaN"))
        row.extend(qe_roc)

        current_mc, mc_roc = quarterly_market_cap_roc(t)
        #print("mc_roc: {}".format(mc_roc))
        for i in range(len(mc_roc), 4):
            row.append(float("NaN"))
        row.extend(mc_roc)
        row.append(current_mc)
            
        if debug:
            print("row {}".format(row))
        df.loc[t] = row
    return df

#tickers = ['four', 'stne']
#tickers = ['four']

wind = ['hxl', 'tpic', 'ndx1.de', 'neoen.pa', 'nrg', 'pne3.de', 'bwen', 'bep']
hydrogen = ['afc.l', 'nel.ol', 'itm.l', 'plug', 'be', 'cwr.l', 'bldp', 'fcel', 'pcell.st']
biofuel = ['regi', 'vbk.de']
energy_storage = ['enph', 'eose']
solar = ['arry', 'csiq', 'sedg', 'fslr', 'run', 'spwr', 's92.de', 'azre']

tickers = wind + hydrogen + biofuel + energy_storage + solar
#tickers = biofuel
df = process_tickers(tickers)
print(df)
df.to_csv('stats.csv')
