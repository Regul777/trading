#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 20:14:06 2020

@author: nishant.gupta
"""


# =============================================================================
# Backtesting strategy - I : Monthly portfolio rebalancing
# Author : Mayank Rasu

# Please report bug/issues in the Q&A section
# =============================================================================

import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import datetime
import copy
import matplotlib.pyplot as plt


def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()
    n = len(df)/12
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR

def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    vol = df["mon_ret"].std() * np.sqrt(12)
    return vol

def sharpe(DF,rf):
    "function to calculate sharpe ratio ; rf is the risk free rate"
    df = DF.copy()
    sr = (CAGR(df) - rf)/volatility(df)
    return sr    

def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd

# function to calculate portfolio return iteratively
def pflio(DF,m,x):
    """Returns cumulative portfolio return
    DF = dataframe with monthly return info for all stocks
    m = number of stock in the portfolio
    x = number of underperforming stocks to be removed from portfolio monthly"""
    df = DF.copy()
    portfolio = []
    monthly_ret = [0]
    for i in range(1, len(df)):
        if len(portfolio) > 0:
            monthly_ret.append(df[portfolio].iloc[i,:].mean())
            bad_stocks = df[portfolio].iloc[i,:].sort_values(ascending=True)[:x].index.values.tolist()
            portfolio = [t for t in portfolio if t not in bad_stocks]
        fill = m - len(portfolio)
        new_picks = df.iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
        portfolio = portfolio + new_picks
    monthly_ret_df = pd.DataFrame(np.array(monthly_ret),columns=["mon_ret"])
    return monthly_ret_df

# Download historical data (monthly) for DJI constituent stocks

count = 0
while (count < 5) :
  print("**********Run ", count+1, "************")
  tickers = ["ASIANPAINT.BO", "AXISBANK.BO", "BAJAJ-AUTO.BO", "BAJFINANCE.BO", "BHARTIARTL.BO",
           "HCLTECH.BO", "HDFCBANK.BO", "HEROMOTOCO.BO", "HINDUNILVR.BO", "ICICIBANK.BO", 
           "INDUSINDBK.BO", "INFY.BO", "ITC.BO", "KOTAKBANK.BO", "LT.BO", "M&M.BO", "MARUTI.BO",
           "NESTLEIND.BO", "NTPC.BO", "ONGC.BO", "POWERGRID.BO", "RELIANCE.BO", "SBIN.BO",
           "SUNPHARMA.BO", "TATASTEEL.BO", "TCS.BO", "TECHM.BO", "TITAN.BO", "ULTRACEMCO.BO"]

  ohlc_mon = {} # directory with ohlc value for each stock            
  attempt = 0 # initializing passthrough variable
  drop = [] # initializing list to store tickers whose close price was successfully extracted
  while len(tickers) != 0 and attempt <= 5:
      print("Attempt: ", attempt)
      tickers = [j for j in tickers if j not in drop] # removing stocks whose data has been extracted from the ticker list
      for i in range(len(tickers)):
          try:
              ohlc_mon[tickers[i]] = pdr.get_data_yahoo(tickers[i],datetime.date.today()-datetime.timedelta(1460),datetime.date.today(),interval='m')
              ohlc_mon[tickers[i]].dropna(inplace = True)
              drop.append(tickers[i])       
          except:
              print(tickers[i]," :failed to fetch data...retrying")
      attempt+=1
 
  tickers = ohlc_mon.keys() # redefine tickers variable after removing any tickers with corrupted data

################################Backtesting####################################

# calculating monthly return for each stock and consolidating return info by stock in a separate dataframe
  ohlc_dict = copy.deepcopy(ohlc_mon)
  return_df = pd.DataFrame()
  for ticker in tickers:
      #print("calculating monthly return for ",ticker)
      ohlc_dict[ticker]["mon_ret"] = ohlc_dict[ticker]["Adj Close"].pct_change()
      return_df[ticker] = ohlc_dict[ticker]["mon_ret"]


#calculating overall strategy's KPIs
  temp = pflio(return_df, 25, 25)
  cagr_total = CAGR(temp)
  sharepe_total = sharpe(temp,0.025)
  dd_total = max_dd(temp) 
  print("Run: ", count+1, " CAGR: ", cagr_total, " Sharepe: ", sharepe_total)
  count += 1