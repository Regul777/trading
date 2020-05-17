#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 22:06:45 2020

@author: nishant.gupta
"""

from intrinsic_data import value_investing_data_getter

tickers = ["ASIANPAINT.BO",\
           #"AXISBANK.BO",\
           "BAJAJ-AUTO.BO",\
           "BHARTIARTL.BO",\
           "HCLTECH.BO", \
           #"HDFCBANK.BO",\
           "HEROMOTOCO.BO",\
           "HINDUNILVR.BO",\
           #"INDUSINDBK.BO",\
           "INFY.BO",\
           "ITC.BO",\
           #"KOTAKBANK.BO",\
           "LT.BO",\
           "M&M.BO",\
           "MARUTI.BO",\
           "NESTLEIND.BO",\
           "NTPC.BO",\
           "ONGC.BO",\
           "POWERGRID.BO",\
           #"SBIN.BO",\
           "SUNPHARMA.BO",\
           "TATASTEEL.BO",\
           "TCS.BO",\
           "TECHM.BO",\
           "ULTRACEMCO.BO",\
           #"BAJFINANCE.BO",\
           #"HDFC.BO",\
           #"ICICIBANK.BO",\
           "RELIANCE.BO",\
           "TITAN.BO",\
           "ADANIPORTS.BO",\
           #"BAJAJFINSV.BO",\
           "BPCL.BO",\
           "BRITANNIA.BO",\
           "CIPLA.BO",\
           "COALINDIA.BO",\
           "DRREDDY.BO",\
           "EICHERMOT.BO",\
           "GAIL.BO",\
           "GODREJCP.BO",\
           "GRASIM.BO",\
           "HINDALCO.BO",\
           "HINDUNILVR.BO",\
           #"IBULHSGFIN.BO",\
           "IOC.BO",\
           "JSWSTEEL.BO",\
           "TATAMOTORS.BO",\
           "TATAMTRDVR.BO",\
           "UPL.BO", \
           "VEDL.BO",\
           "WIPRO.BO"]
           #"YESBANK.BO"]

intersting_data_dict, tickers_collated_data, df_list1 = value_investing_data_getter.get_interesting_data(tickers)
df_list1.to_excel("list1.xls")