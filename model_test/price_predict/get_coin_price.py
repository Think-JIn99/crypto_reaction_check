import yfinance as yf
from datetime import datetime
import pandas as pd
coin_list = ['DOGE-USD','BTC-USD','ETH-USD']
_start = datetime(2020,1,1)
_end = datetime(2021,11,1)
for coin in coin_list:
    df = yf.download(coin, start =_start, end =_end)
    df.drop(['Adj Close'],axis = 1,inplace = True)
    df.to_csv(f"./coin_price/{coin}.csv")
