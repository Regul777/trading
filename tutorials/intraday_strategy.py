#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 12:38:06 2020

@author: nishant.gupta
"""

import datetime
import numpy as np 
import pandas_datareader.data as pdr
import pytz

from alpha_vantage.timeseries import TimeSeries
from indicators import Indicator

def massage_ohlv_data(df, meta_data, ticker) :
   # Resetting the index because we want to change it
   # TODO: See if an index can be changed without resetting
   df.reset_index(inplace = True)
   old_timezone = pytz.timezone(meta_data['6. Time Zone'])
   for j in range(len(df)) :
       date = df['date'][j]
       date_new_timezone = old_timezone.localize(date).astimezone(new_timezone)
       date_new_timezone = date_new_timezone.strftime(date_format)
       df['date'][j] = date_new_timezone            
   df = df.iloc[::-1]
   df.columns = ["Date", "Open", "High", "Low", "Adj Close", "Volume"]
   df.set_index("Date", inplace = True)
   return df

key = "055FVQ7KAZK2L85H" # niku2907@gmail.com
key2 = "LTP4AYWJYLX3OE90" # nishantgupta2907@gmail.com
key3 = "GFQ9OUJN122ARRXF" # nishant.gupta.trading@gmail.com

tickers = ["ICICIBANK.BO"]
ohlc_intraday = {} # directory with ohlc value for each stock            
ts = TimeSeries(key = key, output_format = 'pandas')
    
new_timezone = pytz.timezone("Asia/Calcutta")
date_format = '%Y-%m-%d %H:%M:%S'
date_format_dict_key = '%Y-%m-%d'
attempt = 0 # initializing passthrough variable
drop = [] # initializing list to store tickers whose close price was successfully extracted

ohlc_intraday_30_mins= {}
while len(tickers) != 0 and attempt <= 5:
    tickers = [j for j in tickers if j not in drop]
    for i in range(len(tickers)):
        try:
            ohlc_intraday[tickers[i]], meta_data = ts.get_intraday(symbol = tickers[i],\
                                                                   interval='1min',\
                                                                   outputsize='full')            
            ohlc_intraday[tickers[i]] = massage_ohlv_data(ohlc_intraday[tickers[i]], meta_data, tickers[i])
            
            # Getting the 30 min time frame data as well
            ohlc_intraday_30_mins[tickers[i]], meta_data = ts.get_intraday(symbol = tickers[i],\
                                                                           interval='30min',\
                                                                           outputsize='full')
            ohlc_intraday_30_mins[tickers[i]] = massage_ohlv_data(ohlc_intraday_30_mins[tickers[i]], meta_data, tickers[i])            
            drop.append(tickers[i])      
        except:
            print("Couldn't fetch data for: ", tickers[i])
    attempt += 1

 
tickers = ohlc_intraday.keys() # redefine tickers variable after removing any tickers with corrupted data

collated_data = {}
for ticker in tickers:

    # Get the trend line of the short term data
    ohlc_intraday[ticker]["price_slope"]= Indicator.slope(ohlc_intraday[ticker]["Adj Close"], 5)
    ohlc_intraday[ticker]["short_trend"] = np.where(ohlc_intraday[ticker]["price_slope"] > 0, 1, \
                                                        np.where(ohlc_intraday[ticker]["price_slope"] < 0, -1, 0))
    for i in range(1,len(ohlc_intraday[ticker]["short_trend"])):
          if ohlc_intraday[ticker]["short_trend"][i] > 0 and \
             ohlc_intraday[ticker]["short_trend"][i-1] > 0:
            ohlc_intraday[ticker]["short_trend"][i] += ohlc_intraday[ticker]["short_trend"][i-1]
          elif ohlc_intraday[ticker]["short_trend"][i] < 0 and \
               ohlc_intraday[ticker]["short_trend"][i-1] < 0:
            ohlc_intraday[ticker]["short_trend"][i] += ohlc_intraday[ticker]["short_trend"][i-1]
   
    # Get the trend line of the mid frame
    ohlc_intraday_30_mins[ticker]["price_slope"]= Indicator.slope(ohlc_intraday_30_mins[ticker]["Adj Close"], 5)
    ohlc_intraday_30_mins[ticker]["long_trend"] = np.where(ohlc_intraday_30_mins[ticker]["price_slope"] > 0, 1, \
                                                        np.where(ohlc_intraday_30_mins[ticker]["price_slope"] < 0, -1, 0))
    for i in range(1,len(ohlc_intraday_30_mins[ticker]["long_trend"])):
          if ohlc_intraday_30_mins[ticker]["long_trend"][i] > 0 and \
             ohlc_intraday_30_mins[ticker]["long_trend"][i-1] > 0:
            ohlc_intraday_30_mins[ticker]["long_trend"][i] += ohlc_intraday_30_mins[ticker]["long_trend"][i-1]
          elif ohlc_intraday_30_mins[ticker]["long_trend"][i] < 0 and \
               ohlc_intraday_30_mins[ticker]["long_trend"][i-1] < 0:
            ohlc_intraday_30_mins[ticker]["long_trend"][i] += ohlc_intraday_30_mins[ticker]["long_trend"][i-1]
    
    # Getting 30 days exponential moving average
    # Taking the price of delta days back coz. of the conditon market is right now
    interday_data_for_ticker = pdr.get_data_yahoo(ticker, datetime.date.today() - datetime.timedelta(200), datetime.date.today())
    interday_data_for_ticker.reset_index(inplace = True)
    interday_data_for_ticker = interday_data_for_ticker.iloc[:,[0, 6]]
    
    for i in range(len(interday_data_for_ticker)) :
        date = interday_data_for_ticker['Date'][i]
        date = date.strftime(date_format_dict_key)
        interday_data_for_ticker['Date'][i] = str(date)
    interday_data_for_ticker.set_index("Date", inplace = True)
    
    ohlc_intraday[ticker]['EMA'] = 0.0
    ohlc_intraday[ticker]['MT'] = 'NA'
    
    # Getting exponential MA for 30 days
    ema = interday_data_for_ticker['Adj Close'].ewm(span = 50, adjust = False, min_periods = 50).mean().dropna()
    ema_dict = ema.to_dict()
   
    ohlc_intraday[ticker].reset_index(inplace = True)
    ohlc_intraday_30_mins[ticker].reset_index(inplace = True)
    # Now fill the EMA column in ohlc_intraday
    for i in range(len(ohlc_intraday[ticker])) :
        date = ohlc_intraday[ticker]['Date'][i]
        date = date.split(' ')     
        ohlc_intraday[ticker]['EMA'][i] = ema_dict[date[0]]
        if (ohlc_intraday[ticker]['Adj Close'][i] < ohlc_intraday[ticker]['EMA'][i]):
            ohlc_intraday[ticker]['MT'][i] = 'D'
        else :
            ohlc_intraday[ticker]['MT'][i] = 'U'
            
    collated_data[ticker] = ohlc_intraday[ticker].merge(ohlc_intraday_30_mins[ticker].loc[:,["Date","long_trend"]], \
                                                        how="outer", on="Date")
    collated_data[ticker]["long_trend"].fillna(method='ffill', inplace=True)