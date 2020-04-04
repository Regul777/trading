#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:47:54 2020

@author: nishant.gupta
"""

import numpy as np
import statsmodels.api as sm

from fibonacci_retracement import fib_levels_helper
from stocktrends import Renko

class Indicator:
  def ATR(DF, n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L'] = abs(df['High']-df['Low'])
    df['H-PC'] = abs(df['High']-df['Adj Close'].shift(1))
    df['L-PC'] = abs(df['Low']-df['Adj Close'].shift(1))
    df['TR'] = df[['H-L','H-PC','L-PC']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'], axis=1)
    return df2

  def slope(ser,n):
    "function to calculate the slope of n consecutive points on a plot"
    slopes = [i*0 for i in range(n-1)]
    for i in range(n,len(ser)+1):
        y = ser[i-n:i]
        x = np.array(range(n))
        y_scaled = (y - y.min())/(y.max() - y.min())
        x_scaled = (x - x.min())/(x.max() - x.min())
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled,x_scaled)
        results = model.fit()
        slopes.append(results.params[-1])
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slope_angle)

  def renko_DF(DF):
    "function to convert ohlc data into renko bricks"
    try:
        print("Nishant")
        df = DF.copy()
        df.reset_index(inplace=True)
        df = df.iloc[:,[0,1,2,3,4,5]]
        df.columns = ["date","open","high","low","close","volume"]
        
        df2 = Renko(df)
        
        # TODO: Investigate what brick size is good
        df2.brick_size = max(5, round(Indicator.ATR(DF, 120)["ATR"][-1], 0))
        print("Brick size: ", df2.brick_size)
        renko_df = df2.get_ohlc_data()
        renko_df["bar_num"] = np.where(renko_df["uptrend"] == True, 1, np.where(renko_df["uptrend"] == False, -1, 0))
        for i in range(1,len(renko_df["bar_num"])):
          if renko_df["bar_num"][i] > 0 and renko_df["bar_num"][i-1] > 0:
            renko_df["bar_num"][i] += renko_df["bar_num"][i-1]
          elif renko_df["bar_num"][i] < 0 and renko_df["bar_num"][i-1] < 0:
            renko_df["bar_num"][i] += renko_df["bar_num"][i-1]
        renko_df.drop_duplicates(subset="date",keep="last", inplace=True)
        return renko_df
    except :
        print("Failed to get renko")

  def OBV(DF):
    """function to calculate On Balance Volume"""
    df = DF.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()
    df['direction'] = np.where(df['daily_ret'] >= 0, 1, -1)
    df['direction'][0] = 0
    df['vol_adj'] = df['Volume'] * df['direction']
    df['obv'] = df['vol_adj'].cumsum()
    return df['obv']

  def RSI(DF,n):
    "function to calculate RSI"
    df = DF.copy()
    df['delta'] = df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain'] = np.where(df['delta'] >= 0, df['delta'], 0)
    df['loss']= np.where(df['delta'] < 0, abs(df['delta']), 0)
    avg_gain = []
    avg_loss = []
    gain = df['gain'].tolist()
    loss = df['loss'].tolist()
    for i in range(len(df)):
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
            avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
        elif i > n:
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
    df['avg_gain'] = np.array(avg_gain)
    df['avg_loss'] = np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    return df['RSI']

  def ADX(DF,n):
    "function to calculate ADX"
    df2 = DF.copy()
    df2['TR'] = Indicator.ATR(df2,n)['TR'] #the period parameter of ATR function does not matter because period does not influence TR calculation
    df2['DMplus'] = np.where((df2['High']-df2['High'].shift(1)) > (df2['Low'].shift(1) - df2['Low']), df2['High'] - df2['High'].shift(1), 0)
    df2['DMplus'] = np.where(df2['DMplus']<0,0,df2['DMplus'])
    df2['DMminus'] = np.where((df2['Low'].shift(1) - df2['Low']) > (df2['High'] - df2['High'].shift(1)), df2['Low'].shift(1) - df2['Low'], 0)
    df2['DMminus'] = np.where(df2['DMminus'] < 0, 0, df2['DMminus'])
    TRn = []
    DMplusN = []
    DMminusN = []
    TR = df2['TR'].tolist()
    DMplus = df2['DMplus'].tolist()
    DMminus = df2['DMminus'].tolist()
    for i in range(len(df2)):
        if i < n:
            TRn.append(np.NaN)
            DMplusN.append(np.NaN)
            DMminusN.append(np.NaN)
        elif i == n:
            TRn.append(df2['TR'].rolling(n).sum().tolist()[n])
            DMplusN.append(df2['DMplus'].rolling(n).sum().tolist()[n])
            DMminusN.append(df2['DMminus'].rolling(n).sum().tolist()[n])
        elif i > n:
            TRn.append(TRn[i-1] - (TRn[i-1]/n) + TR[i])
            DMplusN.append(DMplusN[i-1] - (DMplusN[i-1]/n) + DMplus[i])
            DMminusN.append(DMminusN[i-1] - (DMminusN[i-1]/n) + DMminus[i])
    df2['TRn'] = np.array(TRn)
    df2['DMplusN'] = np.array(DMplusN)
    df2['DMminusN'] = np.array(DMminusN)
    df2['DIplusN'] = 100*(df2['DMplusN']/df2['TRn'])
    df2['DIminusN'] = 100*(df2['DMminusN']/df2['TRn'])
    df2['DIdiff'] = abs(df2['DIplusN']-df2['DIminusN'])
    df2['DIsum'] = df2['DIplusN']+df2['DIminusN']
    df2['DX'] = 100*(df2['DIdiff']/df2['DIsum'])
    ADX = []
    DX = df2['DX'].tolist()
    for j in range(len(df2)):
        if j < 2*n-1:
            ADX.append(np.NaN)
        elif j == 2*n-1:
            ADX.append(df2['DX'][j-n+1:j+1].mean())
        elif j > 2*n-1:
            ADX.append(((n-1)*ADX[j-1] + DX[j])/n)
    df2['ADX']=np.array(ADX)
    return df2['ADX']

  def Fib_levels(DF) :
    df2 = DF.copy()
    R1 = []
    S1 = []
    R2 = []
    S2 = []
    R3 = []
    S3 = []
    R1.append('NA')
    S1.append('NA')
    R2.append('NA')
    S2.append('NA')
    R3.append('NA')
    S3.append('NA')
    for i in range(1, len(df2)):
      prev_high = df2['High'][i-1]
      prev_low = df2['Low'][i-1]
      uptrend = False
      if (df2['bar_num'][i-1] >= 4) :
        print("Assuming stock to be in uptrend while calculating fibonacci levels")
        uptrend = True
      else :
        print("Assuming stock to be in downtrend while calculating fibonacci levels")
      fib_levels = fib_levels_helper.get(prev_high, prev_low, uptrend)
      R1.append(fib_levels.RS1.resistance)
      S1.append(fib_levels.RS1.support)
      R2.append(fib_levels.RS2.resistance)
      S2.append(fib_levels.RS2.support)
      R3.append(fib_levels.RS3.resistance)
      S3.append(fib_levels.RS3.support)
      #print("R1: ", temp.RS1.resistance, " S1: ", temp.RS1.support)

    df2['R1'] = R1
    df2['S1'] = S1
    df2['R2'] = R2
    df2['S2'] = S2
    df2['R3'] = R3
    df2['S3'] = S3
    return df2  