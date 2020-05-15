#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 22:18:25 2020

@author: nishant.gupta
"""

from intrinsic_data import value_investing_data_getter

tickers = ["ADANIPOWER.BO",\
           "ADANITRANS.BO",\
           "BHEL.BO",\
           "CESC.BO",\
           "KALPATPOWER.BO",\
           "KEC.BO",\
           "NHPC.BO",\
           "NTPC.BO",\
           "POWERGRID.BO",\
           "SIEMENS.BO",\
           "TATAPOWER.BO",\
           "THERMAX.BO",\
           "TORNTPOWER.BO"]

intersting_data_dict, tickers_collated_data, df = value_investing_data_getter.get_interesting_data(tickers)