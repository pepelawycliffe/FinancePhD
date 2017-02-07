
import pandas as pd
import seaborn as sns
from pymongo import MongoClient
from datetime import datetime
from arctic import Arctic
from pandas_highcharts.core import serialize

def equity_markets_charts(div,library):
    key_markets=['FTSE 100','S&P 500','Russell 2000','EuroStoxx 50']
    df=pd.DataFrame()
    for mkt in key_markets:
        try:
            df[mkt]=library.read(mkt).data.Price
        except:
            print mkt        
    data=df.ffill()['2016':]/df.ffill()['2016':].ix[0]
    return serialize(data,render_to=div,title='Equities YTD',output_type='json')

def zscore_ranked(div,library):
    data=pd.DataFrame()
    for mkt in library.list_symbols():
        try:
            data[mkt]=library.read(mkt).data.Price
        except:
            print mkt
    zscores=(data-pd.ewma(data,20))/pd.ewmstd(data,20)
    latest=zscores.tail(2)
    zscore_ranked=latest.T.sort_values(by=latest.T.columns[0]).dropna()[:5]
    zscore_ranked=zscore_ranked.append(latest.T.sort_values(by=latest.T.columns[0]).dropna()[-5:])
    return serialize(zscore_ranked,render_to=div, kind="bar", title="Noteable market moves",output_type='json')