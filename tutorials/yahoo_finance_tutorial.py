#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:00:32 2020

@author: nishant.gupta
"""

import pandas as pd
from yahoofinancials import YahooFinancials
import datetime

end_date = (datetime.date.today()).strftime('%Y-%m-%d')
start_date = (datetime.date.today() - datetime.timedelta(1025)).strftime('%Y-%m-%d')
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
          yahoo_financials = YahooFinancials(cp_tickers[i])
          json_obj = yahoo_financials.get_historical_stock_data(start_date, end_date, 'daily')
          ohlv = json_obj[cp_tickers[i]]['prices']
          temp_data = pd.DataFrame(ohlv)[["formatted_date", "open", "high", "low", "close", "adjclose"]]
          temp = [cp_tickers[i], temp_data]
          output.append(temp)
          drop.append(cp_tickers[i])
      except:
          print(cp_tickers[i], ": failed to get the data")
    attempt += 1


