#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 12:36:58 2020

@author: nishant.gupta
"""


import pandas as pd
import pandas_datareader.data as pdr
import datetime

class yahoo_finance_data_getter :
   @staticmethod
   def get_historical_data(tickers, num_days = 200) :
    close_prices = pd.DataFrame()
    attempt = 0
    drop = []
    while len(tickers) != 0 and attempt <= 5:
      tickers = [j for j in tickers if j not in drop]
      for i in range(len(tickers)):
        try:
          print("Getting Historic data for : ", tickers[i], " for ", num_days, " days")
          historic_data = pdr.get_data_yahoo(tickers[i], datetime.date.today()-datetime.timedelta(num_days), datetime.date.today())
          historic_data.dropna(inplace = True)
          close_prices[tickers[i]] = historic_data["Adj Close"]
          drop.append(tickers[i])       
        except:
          print(tickers[i]," :failed to fetch data...retrying")
    attempt += 1
    return close_prices

   @staticmethod
   def get_mean_data(tickers, num_days = 200) :
     closing_prices = yahoo_finance_data_getter.get_historical_data(tickers, num_days)
     mean_price_for_each_stock = closing_prices.mean()
     return mean_price_for_each_stock
 
   @staticmethod
   def get_daily_return_data(tickers, num_days = 200) :
     closing_prices = yahoo_finance_data_getter.get_historical_data(tickers, num_days)
     daily_return_for_each_stock = closing_prices.pct_change()
     return daily_return_for_each_stock
 
   @staticmethod
   def get_mean_data_for_ticker(ticker, num_days = 200) :
     print("Getting Mean data for : ", ticker, " over ", num_days, " days")
     historic_data = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(num_days), datetime.date.today())
     historic_data.dropna(inplace = True)
     return historic_data["Adj Close"].mean()
     
 
   @staticmethod
   def get_daily_return_data_for_ticker(ticker, num_days = 200) :
     print("Getting Daily return data for : ", ticker, " for ", num_days, " days")
     historic_data = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(num_days), datetime.date.today())
     historic_data.dropna(inplace = True)
     return historic_data["Adj Close"].pct_change()
       
        
