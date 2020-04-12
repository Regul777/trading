#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:05:47 2020

@author: nishant.gupta
"""

import copy
import datetime
import math
import pandas_datareader.data as pdr

from fibonacci_retracement import fib_levels_helper
from mail_utils import smtp_client
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
      
      # Putting the MACD data into the ohlc_renko frame
      ohlc_renko[ticker]["macd"]= Indicator.MACD(ohlc_renko[ticker], 12, 26, 9)[0]
      ohlc_renko[ticker]["macd_sig"]= Indicator.MACD(ohlc_renko[ticker],12, 26, 9)[1]
      ohlc_renko[ticker]["macd_slope"] = Indicator.slope(ohlc_renko[ticker]["macd"], 5)
      ohlc_renko[ticker]["macd_sig_slope"] = Indicator.slope(ohlc_renko[ticker]["macd_sig"], 5)
      
      #collated_data[ticker] = ohlc_renko[ticker].iloc[:, [3, 5, 6, 8, 9, 10]]
      collated_data[ticker] = Indicator.Fib_levels(ohlc_renko[ticker])
      #collated_data[ticker] = collated_data[ticker].iloc[:, [3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]]
      #collated_data[ticker] = collated_data[ticker].iloc[:, [0, 5]]
      collated_data[ticker].set_index("Date", inplace = True)
      collated_data[ticker] = collated_data[ticker].iloc[:, [0, 1, 2, 3,5,7,8,9,10,11,12,13,14,15,16,17,18,19]]
      tickers_state[ticker] = []
      tickers_ret[ticker] = []
      tickers_signal[ticker] = []
      
    return interday_data(tickers, collated_data, ohlc_renko, tickers_ret, tickers_state, tickers_signal)

  @staticmethod
  def get_last_two_days_data(ohlc_data, tickers) :
      last_two_days_data = {}
      for ticker in tickers:
          ticker_data = ohlc_data[ticker].iloc[:, [3, 8, 9, 16]]
          last_two_days_ticker_data = ticker_data.tail(2)
          last_two_days_data[ticker] = last_two_days_ticker_data
      return last_two_days_data
  
  @staticmethod
  def get_interesting_stocks(ohlc_data, tickers) :
      last_two_days_data = interday_testing_helper.get_last_two_days_data(ohlc_data, tickers)
      buy_stocks = {}
      sell_stocks = {}
      buy_prev_price = []
      sell_prev_price = []
      for ticker in tickers:
          ticker_data = last_two_days_data[ticker]
          last_day_data = ticker_data.tail(1)
          second_last_day_data = ticker_data.head(1)
          prev_close_price = second_last_day_data['Adj Close'][0]
          signal = last_day_data['Signal'][0]
          if (signal == 'S' or signal == 'B') :
              if (signal == 'S') :
                  sell_prev_price.append(prev_close_price)
                  sell_stocks[ticker] = last_day_data
                  sell_stocks[ticker]['Prev_Close'] = prev_close_price
              else :
                  buy_prev_price.append(prev_close_price)
                  buy_stocks[ticker] = last_day_data
                  buy_stocks[ticker]['Prev_Close'] = prev_close_price
      return buy_stocks, sell_stocks
  
  @staticmethod
  def send_mail_for_interesting_stocks(cummulative_ohlc_data, tickers, is_v1 = True):
      buy_stocks, sell_stocks = interday_testing_helper.get_interesting_stocks(cummulative_ohlc_data, tickers)
      if (len(buy_stocks) > 0):
          stocks = ""
          for ticker in buy_stocks:
              message = ticker
              message += " Current: " + str(math.floor(buy_stocks[ticker]['Adj Close']))
              message += " Prev: " + str(math.floor(buy_stocks[ticker]['Prev_Close']))
              message += " RSI: " + str(math.floor(buy_stocks[ticker]['RSI']))
              message += " ADX: " + str(math.floor(buy_stocks[ticker]['ADX']))
              stocks += message
              stocks += "\n"
          subject = "Buy these stocks"
          if (is_v1 == True) :
              subject += "(V1)"
          else:
              subject += "(V2)"
          smtp_client.send_mail("niku2907@gmail.com", stocks, subject)

      if (len(sell_stocks) > 0):
          stocks = ""
          for ticker in sell_stocks:
              message = ticker
              message += " Current: " + str(math.floor(sell_stocks[ticker]['Adj Close']))
              message += " Prev: " + str(math.floor(sell_stocks[ticker]['Prev_Close']))
              message += " RSI: " + str(math.floor(sell_stocks[ticker]['RSI']))
              message += " ADX: " + str(math.floor(sell_stocks[ticker]['ADX']))
              stocks += message
              stocks += "\n"
          subject = "Sell these stocks"
          if (is_v1 == True) :
              subject += "(V1)"
          else:
              subject += "(V2)"
          smtp_client.send_mail("niku2907@gmail.com", stocks, subject)
          
      # Next day's Ri/Si is also an interesting data point
      last_days_data = {}
      for ticker in tickers:
          ticker_data = cummulative_ohlc_data[ticker]
          last_days_ticker_data = ticker_data.tail(1)
          last_days_data[ticker] = last_days_ticker_data
    
      ticker_RS_levels = ""
      for ticker in tickers:
          print("Ticker: ", ticker)
          ticker_data = last_days_data[ticker]
          prev_high = ticker_data['High'][0]
          prev_low = ticker_data['Low'][0]
          uptrend = False
          if (ticker_data['bar_num'][0] >= 4) :
              print("Assuming stock to be in uptrend while calculating fibonacci levels")
              uptrend = True
          else :
              print("Assuming stock to be in downtrend while calculating fibonacci levels")
        
          fib_levels = fib_levels_helper.get(prev_high, prev_low, uptrend)
          ticker_RS_levels += ticker
          ticker_RS_levels += " (R1 = " + str(math.floor(fib_levels.RS1.resistance)) + " ,S1 = " + str(math.floor(fib_levels.RS1.support)) + ") "
          ticker_RS_levels += " (R2 = " + str(math.floor(fib_levels.RS2.resistance)) + " ,S2 = " + str(math.floor(fib_levels.RS2.support)) + ") "
          ticker_RS_levels += " (R3 = " + str(math.floor(fib_levels.RS3.resistance)) + " ,S3 = " + str(math.floor(fib_levels.RS3.support)) + ") "
          ticker_RS_levels += "\n"
      smtp_client.send_mail("niku2907@gmail.com", ticker_RS_levels, "Potential R/S levels for next days")