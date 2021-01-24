import pandas as pd
from revenue import quarterly_revenues_roc
from market_cap import quarterly_market_cap_roc
import yahoo_fin.stock_info as si
import urllib
import time

debug = False


def process_ticker(t):
    print("Processing {}".format(t))
    row = []

    qe_roc = quarterly_revenues_roc(t)
    #print("qe_roc: {}".format(qe_roc))
    for i in range(len(qe_roc), 3):
        row.append(float("NaN"))
    row.extend(qe_roc)

    time.sleep(15)

    current_mc, mc_roc = quarterly_market_cap_roc(t)
    #print("mc_roc: {}".format(mc_roc))
    for i in range(len(mc_roc), 4):
        row.append(float("NaN"))
    row.extend(mc_roc)
    row.append(current_mc)

    time.sleep(15)

    quote_table = si.get_quote_table(t)
    row.append(quote_table['EPS (TTM)'])

    time.sleep(15)

    try:
        stats = si.get_stats(t)
        revenue_per_share = stats.loc['Revenue Per Share (ttm)' ==
                                      stats.Attribute]['Value'].values[0]
        row.append(revenue_per_share)
    except ValueError:
        print('error retrieving revenue per share.')
        row.append('')

    time.sleep(15)

    if debug:
        print("row {}".format(row))

    return row


def process_tickers(tickers):
    df = pd.DataFrame(columns=[
        'R:Q-3', 'R:Q-2', 'R:Q-1', 'MC:Q-3', 'MC:Q-2', 'MC:Q-1', 'MC:Q-0',
        'MC:current', 'EPS', 'RevenuePerShare'
    ])
    df.index.name = 'ticker'
    error_encountered = 0
    index = 0
    while index < len(tickers):
        t = tickers[index]
        try:
            df.loc[t] = process_ticker(t)
            index += 1
        except urllib.error.HTTPError as e:
            print(e)
            time.sleep(600)
            error_encountered += 1
            if error_encountered > 3:
                break
    return df


#tickers = ['four', 'stne']
#tickers = ['four']

solar = [
    'arry', 'csiq', 'enph', 'sedg', 'fslr', 'run', 'spwr', 's92.de', 'azre',
    'dq', 'sol.mc', 'spk.mc', 'nova', 'maxn', 'sol', 'slr.mc', 'wndw', 'sunw'
]
wind = [
    'vwdry', 'sgre.mc', 'hxl', 'tpic', 'ndx1.de', 'neoen.pa', 'nrg', 'pne3.de',
    'bwen', 'bep', 'eolu-b.st', 'ge'
]
hydrogen = [
    'afc.l', 'nel.ol', 'itm.l', 'plug', 'be', 'cwr.l', 'bldp', 'fcel',
    'pcell.st', 'efuel.ol', 'f3c.de'
]
biofuel = ['regi', 'vbk.de', 'ce2.de', 'eqt.l', 'cva']
natural_gas = ['clne']
renewable_devs = [
    'orsted.co', 'ine.to', 'blx.to', 'npi.to', 'cwen', 'mel.nz', 'ora', 'hasi',
    'amrc', 'rwe.de', 'tenergy.at', 'org.nx', 'ay', 'eqnr', 'ana.mc'
]

energy_storage = [
    'enph', 'eose', 'clsk', 'gnrc', 'pola', 'pps.l', 'egt.v', 'egt.v'
]

ev = ['aptv', 'nio', 'nfi.to', 'gp', 'xl', '1211.hk', 'hyln']
ev_battery = ['zap.ol', 'beem', 'asl.f', 'rmo', '006400.KS', '051910.KS']

misc = ['cpst', 'dnmr']

tickers = solar + wind + hydrogen + biofuel + natural_gas + renewable_devs + ev + ev_battery + energy_storage + misc

df = process_tickers(tickers)
print(df)

df.to_csv('stats.csv')
