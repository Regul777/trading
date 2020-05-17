#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 22:19:19 2020

@author: nishant.gupta
"""

from intrinsic_data import value_investing_data_getter

tickers = ["BPCL.BO",\
           "CASTROLIND.BO",\
           "GAIL.BO",\
           "GSPL.BO",\
           "HINDPETRO.BO",\
           "IGL.BO",\
           "IOC.BO",\
           "ONGC.BO",\
           "PETRONET.BO",\
           "RELIANCE.BO"]

intersting_data_dict, tickers_collated_data, df_oil_gas = value_investing_data_getter.get_interesting_data(tickers)
df_oil_gas.to_excel("oil_gas.xls")