#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:05:47 2020

@author: nishant.gupta
"""

import copy
import datetime
import pandas_datareader.data as pdr

from indicators import Indicator

class interday_data:
  def __init__(self, tickers, collated_data, ohlc_renko, tickers_ret, tickers_state, tickers_signal) :
    self.tickers = tickers
    self.collated_data = collated_data
    self.ohlc_renko = ohlc_renko
    self.tickers_ret = tickers_ret
    self.tickers_state = tickers_state
    self.tickers_signal = tickers_signal
      
class interday_testing_helper :
  @staticmethod
  def get_interday_collated_data(tickers, n, delta) :
    attempt = 0
    drop = []
    ohlc_interday = {}
    while len(tickers) != 0 and attempt <=1:
      tickers = [j for j in tickers if j not in drop]
      for i in range(len(tickers)) :
        try:
          # Taking the price of delta days back coz. of the conditon market is right now
          ohlc_interday[tickers[i]] = pdr.get_data_yahoo(tickers[i],datetime.date.today() - datetime.timedelta(n), datetime.date.today() - datetime.timedelta(delta))
          ohlc_interday[tickers[i]] = ohlc_interday[tickers[i]].iloc[:, [2, 0, 1, 5, 4]]
          ohlc_interday[tickers[i]].index.names = ['date']
        except:
          print("Couldn't fetch data for: ", tickers[i])
      attempt += 1

    # These are tickers for which we could fetch the data from yahoo finance
    tickers = ohlc_interday.keys()

    #Merging renko df with the ohlc table
    ohlc_renko = {}
    df = copy.deepcopy(ohlc_interday)
    collated_data = {}
    tickers_ret = {}
    tickers_state = {}
    tickers_signal = {}
    for ticker in tickers:
      renko = Indicator.renko_DF(df[ticker])
      renko.columns = ["Date","open","high","low","close","uptrend","bar_num"]
      df[ticker]["Date"] = df[ticker].index
      ohlc_renko[ticker] = df[ticker].merge(renko.loc[:,["Date","bar_num"]], how="outer", on="Date")
    
      # RSI is for last 14 days
      # RSI > 70 : overbought
      # RSI < 30 : oversold
      rsi = Indicator.RSI(df[ticker], 14)
      rsi_frame = rsi.to_frame()
      rsi_frame.reset_index(inplace = True)
      rsi_frame.columns = ["Date", "RSI"]
    
      # ADX (trend) is also for last 14 days
      # 0-25: Weak
      # 25-50: Strong
      # > 50: Very strong
      adx = Indicator.ADX(df[ticker], 14)
      adx.index.names = ['Date']
      adx_frame = adx.to_frame()
      adx_frame.reset_index(inplace=True)
      adx_frame.column = ["Date", "ADX"]
    
      # "bar_num" column is based on renko chart which has brick size based on ATR (see renko function above)
      ohlc_renko[ticker]["bar_num"].fillna(method='ffill', inplace=True)
      ohlc_renko[ticker]["obv"]= Indicator.OBV(ohlc_renko[ticker])
    
      # obv slope takes last 5 points into consideration
      ohlc_renko[ticker]["obv_slope"]= Indicator.slope(ohlc_renko[ticker]["obv"], 5)
    
      # Merging the RSI data
      ohlc_renko[ticker] = ohlc_renko[ticker].merge(rsi_frame.loc[:,["Date","RSI"]], how="outer", on="Date")
    
      # Merging the ADX data
      ohlc_renko[ticker] = ohlc_renko[ticker].merge(adx_frame.loc[:,["Date","ADX"]], how="outer", on="Date")
      #collated_data[ticker] = ohlc_renko[ticker].iloc[:, [3, 5, 6, 8, 9, 10]]
      collated_data[ticker] = Indicator.Fib_levels(ohlc_renko[ticker])
      #collated_data[ticker] = collated_data[ticker].iloc[:, [3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]]
      #collated_data[ticker] = collated_data[ticker].iloc[:, [0, 5]]
      collated_data[ticker].set_index("Date", inplace = True)
      collated_data[ticker] = collated_data[ticker].iloc[:, [0, 1, 2, 3,5,7,8,9,10,11,12,13,14,15]]
      tickers_state[ticker] = []
      tickers_ret[ticker] = []
      tickers_signal[ticker] = []
      
    return interday_data(tickers, collated_data, ohlc_renko, tickers_ret, tickers_state, tickers_signal)

    