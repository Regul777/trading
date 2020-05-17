#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 02:14:58 2020

@author: nishant.gupta
"""

from intrinsic_data import value_investing_data_getter

tickers = ["ADFFOODS.BO",\
            "APOLLO.BO",\
            "ARVSMART.BO",\
            "CENTURYPLY.BO",\
            "CGCL.BO",\
            "DBREALTY.BO",\
            "DEEPALFERT.BO",\
            "DFM.BO",\
            "DHANUKA.BO",\
            "FELDVR.BO",\
            "GAYAPROJ.BO",\
            "HIKAL.BO",\
            "HLVLTD.BO",\
            "INDIACEM.BO",\
            "INOXWIND.BO",\
            "JBMA.BO",\
            "JISLDVREQS.BO",\
            "JUBILANT.BO",\
            "JISLJALEQS.BO",\
            "KRIINFRA.BO",\
            "MCLEODRUSS.BO",\
            "MUKANDLTD.BO",\
            "NFL.BO",\
            "PROZONINTU.BO",\
            "RANKY.BO",\
            "RCF.BO",\
            "SADBHAV.BO",\
            "SALASAR.BO",\
            "SANGHIIND.BO",\
            "SEYAIND.BO",\
            "SKIPPER.BO",\
            "SPENCER.BO",\
            "TAJGVK.BO",\
            "ZENSARTECH.BO"]

intersting_data_dict, tickers_collated_data, df_small_cap = value_investing_data_getter.get_interesting_data(tickers)
df_small_cap.to_excel("small_cap.xls")                         