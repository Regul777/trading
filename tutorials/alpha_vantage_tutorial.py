#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:12:30 2020

@author: nishant.gupta
"""


import pandas as pd
from alpha_vantage.timeseries import TimeSeries

all_tickers = ["AAPL", "AMZN", "MSFT", "GOOGLE"]
cp_tickers = all_tickers
attempt = 0
drop = []
output = []
while len(cp_tickers) != 0 and attempt <= 5:
    print("Starting attempt: ", attempt)
    cp_tickers = [j for j in cp_tickers if j not in drop]
    for i in range(len(cp_tickers)):
        print("i: ", i)
        try:
            ts = TimeSeries(key="055FVQ7KAZK2L85H", output_format = 'pandas')
            data, metadata = ts.get_intraday(cp_tickers[i], interval = '1min', outputsize = 'full')
            data.columns = ["open", "high", "low", "close", "volume"]
            temp = [cp_tickers[i], data]
            output.append(temp)
            drop.append(cp_tickers[i])
        except:
            print(cp_tickers[i], ": failed to get the data")
    attempt += 1
            