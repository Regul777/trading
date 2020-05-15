#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 22:17:14 2020

@author: nishant.gupta
"""

from intrinsic_data import value_investing_data_getter

tickers = ["DLF.BO",\
           "GODREJPROP.BO",\
           "IBREALEST.BO",\
           "MAHLIFE.BO",\
           "OBEROIRLTY.BO",\
           "OMAXE.BO",\
           "PHOENIXLTD.BO",\
           "PRESTIGE.BO",\
           "SOBHA.BO",\
           "SUNTECK.BO"]

intersting_data_dict, tickers_collated_data, df = value_investing_data_getter.get_interesting_data(tickers)