#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 22:20:16 2020

@author: nishant.gupta
"""

from intrinsic_data import value_investing_data_getter

tickers = ["COALINDIA.BO",\
           "HINDALCO.BO",\
           "HINDZINC.BO",\
           "JINDALSTEL.BO",\
           "JSWSTEEL.BO",\
           "NATIONALUM.BO",\
           "NMDC.BO",\
           "SAIL.BO",\
           "TATASTEEL.BO",\
           "VEDL.BO"]

intersting_data_dict, tickers_collated_data, df = value_investing_data_getter.get_interesting_data(tickers)