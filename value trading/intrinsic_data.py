#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 18:27:16 2020

@author: nishant.gupta
"""

import pandas as pd
from ticker_data import ticker_data_getter

class intersting_data:
    def __init__(self, pe, industry_pe, de, bv, price, intrinsic_val):
        self.pe = pe
        self.industry_pe = industry_pe
        self.de = de
        self.bv = bv
        self.price = price
        self.intrinsic_val = intrinsic_val

class value_investing_data_getter:
    def get_interesting_data(tickers):
        interesting_data_tickers = {}
        num_retries = 10
        ctr = 0
        # For now even if a ticker got error from get_intrinsic_value_of_ticker we will retry the full
        # batch but we can optimize here to retry only the failed ones. 
        while (ctr < num_retries):
            try:
                tickers_collated_data = ticker_data_getter.get_intrinsic_value_of_tickers(tickers)
                break
            except:
                print("Retrying for: ", ctr)
                ctr += 1
        
        print("Got all the financial data. Going to fetch additional data from moneycontrol.")
        # Schema of the data frame is:
        # Ticker    P/E     IP/E    D/E     BV      Price       IntrinsicValue
        eps_list = []
        pe_list = []
        industry_pe_list = []
        de_list = []
        book_value_list = []
        price_list = []
        intrinsic_value_list = []
        ticker_list = []
        columns = ['Ticker', 'EPS', 'P/E', 'IP/E', 'D/E', 'BV', 'Market value', 'Intrinsic value']
        for ticker in tickers_collated_data.keys():
            try:
                debt_to_equity_ratio = tickers_collated_data[ticker].Wd
                eps, pe, industry_pe, book_value = \
                    ticker_data_getter.get_additional_ticker_data_from_moneycontrol(ticker)
                interesting_data_tickers[ticker] = intersting_data(pe = pe,\
                                                                   industry_pe = industry_pe,
                                                                   de = debt_to_equity_ratio,\
                                                                   bv = book_value,\
                                                                   price = \
                                                                       tickers_collated_data[ticker].market_value,\
                                                                   intrinsic_val = \
                                                                       tickers_collated_data[ticker].intrinsic_value)
                ticker_list.append(ticker)
                eps_list.append(eps)
                pe_list.append(pe)
                industry_pe_list.append(industry_pe)
                de_list.append(debt_to_equity_ratio)
                book_value_list.append(book_value)
                price_list.append(tickers_collated_data[ticker].market_value)
                intrinsic_value_list.append(tickers_collated_data[ticker].intrinsic_value)
            except:
                print("Got some error while getting additional data for ticker: ", ticker)
        
        df = pd.DataFrame(list(zip(ticker_list,\
                                   eps_list,\
                                   pe_list,\
                                   industry_pe_list,\
                                   de_list,\
                                   book_value_list,\
                                   price_list,\
                                   intrinsic_value_list)),\
                          columns = columns)
        df.set_index('Ticker', inplace = True)
        return interesting_data_tickers, tickers_collated_data, df

#tickers = ["INFY.BO", "ITC.BO"]
#intersting_data_dict, tickers_collated_data, df = value_investing_data_getter.get_interesting_data(tickers)
       
            
                
            