#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 19:12:02 2020

@author: nishant.gupta
"""


import numpy as np
import pandas as pd
from stocktrends import Renko
import statsmodels.api as sm
from alpha_vantage.timeseries import TimeSeries
import copy
import pandas_datareader.data as pdr
import datetime
import sys

# Following are the indicators and KPIs
def ATR(DF,n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L']=abs(df['High']-df['Low'])
    df['H-PC']=abs(df['High']-df['Adj Close'].shift(1))
    df['L-PC']=abs(df['Low']-df['Adj Close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
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
        
        # TODO: Take brick size as an input to this function based on the stock price
        # We can have it as some percentage of the stock close price
        # df2.brick_size = 5
        df2.brick_size = max(5, round(ATR(DF,120)["ATR"][-1],0))
        renko_df = df2.get_ohlc_data()
        print(renko_df)
        renko_df["bar_num"] = np.where(renko_df["uptrend"]==True,1,np.where(renko_df["uptrend"]==False,-1,0))
        for i in range(1,len(renko_df["bar_num"])):
          if renko_df["bar_num"][i]>0 and renko_df["bar_num"][i-1]>0:
            renko_df["bar_num"][i]+=renko_df["bar_num"][i-1]
          elif renko_df["bar_num"][i]<0 and renko_df["bar_num"][i-1]<0:
            renko_df["bar_num"][i]+=renko_df["bar_num"][i-1]
        renko_df.drop_duplicates(subset="date",keep="last",inplace=True)
        return renko_df
    except :
        print("Failed to get renko")

def OBV(DF):
    """function to calculate On Balance Volume"""
    df = DF.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()
    df['direction'] = np.where(df['daily_ret']>=0,1,-1)
    df['direction'][0] = 0
    df['vol_adj'] = df['Volume'] * df['direction']
    df['obv'] = df['vol_adj'].cumsum()
    return df['obv']

def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    n = len(df)/(252*78)
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR

def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    vol = df["ret"].std() * np.sqrt(252*78)
    return vol

def sharpe(DF,rf):
    "function to calculate sharpe ratio ; rf is the risk free rate"
    df = DF.copy()
    sr = (CAGR(df) - rf)/volatility(df)
    return sr
    

def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd

def RSI(DF,n):
    "function to calculate RSI"
    df = DF.copy()
    df['delta']=df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain']=np.where(df['delta']>=0,df['delta'],0)
    df['loss']=np.where(df['delta']<0,abs(df['delta']),0)
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
    df['avg_gain']=np.array(avg_gain)
    df['avg_loss']=np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    return df['RSI']

def ADX(DF,n):
    "function to calculate ADX"
    df2 = DF.copy()
    df2['TR'] = ATR(df2,n)['TR'] #the period parameter of ATR function does not matter because period does not influence TR calculation
    df2['DMplus']=np.where((df2['High']-df2['High'].shift(1))>(df2['Low'].shift(1)-df2['Low']),df2['High']-df2['High'].shift(1),0)
    df2['DMplus']=np.where(df2['DMplus']<0,0,df2['DMplus'])
    df2['DMminus']=np.where((df2['Low'].shift(1)-df2['Low'])>(df2['High']-df2['High'].shift(1)),df2['Low'].shift(1)-df2['Low'],0)
    df2['DMminus']=np.where(df2['DMminus']<0,0,df2['DMminus'])
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
    df2['DIplusN']=100*(df2['DMplusN']/df2['TRn'])
    df2['DIminusN']=100*(df2['DMminusN']/df2['TRn'])
    df2['DIdiff']=abs(df2['DIplusN']-df2['DIminusN'])
    df2['DIsum']=df2['DIplusN']+df2['DIminusN']
    df2['DX']=100*(df2['DIdiff']/df2['DIsum'])
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

# Fetching the data from yahoo finance
tickers = ["HDFCBANK.BO","INDUSINDBK.BO","ICICIBANK.BO","ITC.BO","AXISBANK.BO"]
ohlc_interday = {}

attempt = 0
drop = []
while len(tickers) != 0 and attempt <=1:
    tickers = [j for j in tickers if j not in drop]
    for i in range(len(tickers)) :
      try:
        ohlc_interday[tickers[i]] = pdr.get_data_yahoo(tickers[i],datetime.date.today()-datetime.timedelta(730),datetime.date.today())
        ohlc_interday[tickers[i]] = ohlc_interday[tickers[i]].iloc[:, [2, 0, 1, 5, 4]]
        ohlc_interday[tickers[i]].index.names = ['date']
        #ohlc_interday[tickers[i]].columns = ["High", "Low", "Open", "Adj Close", "Volume"]
        drop.append(tickers[i]) 
      except:
        print("Couldn't fetch data for: ", tickers[i])
    attempt += 1

tickers = ohlc_interday.keys()

#Merging renko df with the ohlc table
ohlc_renko = {}
df = copy.deepcopy(ohlc_interday)
tickers_signal = {}
tickers_ret = {}
collated_data = {}
for ticker in tickers:
    renko = renko_DF(df[ticker])
    renko.columns = ["Date","open","high","low","close","uptrend","bar_num"]
    df[ticker]["Date"] = df[ticker].index
    ohlc_renko[ticker] = df[ticker].merge(renko.loc[:,["Date","bar_num"]],how="outer",on="Date")
    
    # RSI is for last 14 days
    # RSI > 70 : overbought
    # RSI < 30 : oversold
    rsi = RSI(df[ticker], 14)
    rsi_frame = rsi.to_frame()
    rsi_frame.reset_index(inplace=True)
    rsi_frame.columns = ["Date", "RSI"]
    
    # ADX (trend) is also for last 14 days
    # 0-25: Weak
    # 25-50: Strong
    # > 50: Very strong
    adx = ADX(df[ticker], 14)
    adx.index.names = ['Date']
    adx_frame = adx.to_frame()
    adx_frame.reset_index(inplace=True)
    adx_frame.column = ["Date", "ADX"]
    
    # "bar_num" column is based on renko chart which has brick size based on ATR (see renko function above)
    ohlc_renko[ticker]["bar_num"].fillna(method='ffill', inplace=True)
    ohlc_renko[ticker]["obv"]= OBV(ohlc_renko[ticker])
    
    # obv slope takes last 5 points into consideration
    ohlc_renko[ticker]["obv_slope"]= slope(ohlc_renko[ticker]["obv"], 5)
    
    # Merging the RSI data
    ohlc_renko[ticker] = ohlc_renko[ticker].merge(rsi_frame.loc[:,["Date","RSI"]], how="outer", on="Date")
    
    #Merging the ADX data
    ohlc_renko[ticker] = ohlc_renko[ticker].merge(adx_frame.loc[:,["Date","ADX"]], how="outer", on="Date")
    collated_data[ticker] = ohlc_renko[ticker].iloc[:, [3, 5, 6, 8, 9, 10]]
    collated_data[ticker].set_index("Date", inplace = True)
    tickers_signal[ticker] = []
    tickers_ret[ticker] = []

#Identifying signals and calculating daily return
for ticker in tickers:
    print("calculating daily returns for ",ticker)
    buy = 0
    buy_price = 0
    for i in range(len(ohlc_interday[ticker])):
        if (i < 14):
            tickers_ret[ticker].append(0)
            tickers_signal[ticker].append('NA')
            continue;
        if (buy == 0) :
            tickers_ret[ticker].append(0)            
            #print("RSI: ", ohlc_renko[ticker]["RSI"][i])
            if ohlc_renko[ticker]["RSI"][i] < 30:
                print("Buying the: ", ticker, " at ", ohlc_renko[ticker]["Adj Close"][i])
                print("Bar num: ", ohlc_renko[ticker]["bar_num"][i], "Slope: ", ohlc_renko[ticker]["obv_slope"][i], " RSI: ", ohlc_renko[ticker]["RSI"][i])
                buy = 1
                buy_price = ohlc_renko[ticker]["Adj Close"][i]
                tickers_signal[ticker].append('B')
            else:
                tickers_signal[ticker].append('NA')
        else :
             if ohlc_renko[ticker]["RSI"][i] > 50:
                buy = 0
                tickers_ret[ticker].append((ohlc_renko[ticker]["Adj Close"][i] / buy_price) - 1)
                print("Return booked : ", ohlc_renko[ticker]["Adj Close"][i] / buy_price)
                buy_price = 0
                tickers_signal[ticker].append('S')
             else :
                tickers_ret[ticker].append(0)
                tickers_signal[ticker].append('Hold')
    print("Ticker: ", ticker, "Length: ", len(tickers_signal[ticker]))
    ohlc_renko[ticker]["ret"] = np.array(tickers_ret[ticker])
    ohlc_renko[ticker]["State"] = np.array(tickers_signal[ticker])