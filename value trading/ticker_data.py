#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 00:02:02 2020

@author: nishant.gupta
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd

tickers = ["ASIANPAINT.BO",\
           "AXISBANK.BO",\
           "BAJAJ-AUTO.BO",\
           "BHARTIARTL.BO",\
           "HCLTECH.BO", \
           "HDFCBANK.BO",\
           "HEROMOTOCO.BO",\
           "HINDUNILVR.BO",\
           "INDUSINDBK.BO",\
           "INFY.BO",\
           "ITC.BO",\
           "KOTAKBANK.BO",\
           "LT.BO",\
           "M&M.BO",\
           "MARUTI.BO",\
           "NESTLEIND.BO",\
           "NTPC.BO",\
           "ONGC.BO",\
           "POWERGRID.BO",\
           "SBIN.BO",\
           "SUNPHARMA.BO",\
           "TATASTEEL.BO",\
           "TCS.BO",\
           "TECHM.BO",\
           "ULTRACEMCO.BO",\
           "BAJFINANCE.BO",\
           "HDFC.BO",\
           "ICICIBANK.BO",\
           "RELIANCE.BO",\
           "TITAN.BO",\
           "ADANIPORTS.BO",\
           "BAJAJFINSV.BO",\
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
           "IBULHSGFIN.BO",\
           "IOC.BO",\
           "JSWSTEEL.BO",\
           "TATAMOTORS.BO",\
           "TATAMTRDVR.BO",\
           "UPL.BO", \
           "VEDL.BO",\
           "WIPRO.BO",\
           "YESBANK.BO"]

ticker_symbol_id = dict({"ASIANPAINT.BO":   500820,\
                         "AXISBANK.BO":     532215,\
                         "BAJAJ-AUTO.BO":   532977,\
                         "BHARTIARTL.BO":   532454,\
                         "HCLTECH.BO":      532281,\
                         "HDFCBANK.BO":     500180,\
                         "HEROMOTOCO.BO":   500182,\
                         "HINDUNILVR.BO":   500696,\
                         "INDUSINDBK.BO":   532187,\
                         "INFY.BO":         500209,\
                         "ITC.BO":          500875,\
                         "KOTAKBANK.BO":    500247,\
                         "LT.BO":           500510,\
                         "M&M.BO":          500520,\
                         "MARUTI.BO":       532500,\
                         "NESTLEIND.BO":    500790,\
                         "NTPC.BO":         532555,\
                         "ONGC.BO":         500312,\
                         "POWERGRID.BO":    532898,\
                         "SBIN.BO":         500112,\
                         "SUNPHARMA.BO":    524715,\
                         "TATASTEEL.BO":    500470,\
                         "TCS.BO":          532540,\
                         "TECHM.BO":        532755,\
                         "ULTRACEMCO.BO":   532538,\
                         "BAJFINANCE.BO":   500034,\
                         "HDFC.BO":         500010,\
                         "ICICIBANK.BO":    532174,\
                         "RELIANCE.BO":     500325,\
                         "TITAN.BO":        500114,\
                         "ADANIPORTS.BO":   532921,\
                         "BAJAJFINSV.BO":   532978,\
                         "BPCL.BO":         500547,\
                         "BRITANNIA.BO":    500825,\
                         "CIPLA.BO":        500087,\
                         "COALINDIA.BO":    533278,\
                         "DRREDDY.BO":      500124,\
                         "EICHERMOT.BO":    505200,\
                         "GAIL.BO":         532155,\
                         "GODREJCP.BO":     532424,\
                         "GRASIM.BO":       500300,\
                         "HINDALCO.BO":     500440,\
                         "IBULHSGFIN.BO":   535789,\
                         "IOC.BO":          530965,\
                         "JSWSTEEL.BO":     500228,\
                         "TATAMOTORS.BO":   500570,\
                         "TATAMTRDVR.BO":   570001,\
                         "UPL.BO":          512070,\
                         "VEDL.BO":         500295,\
                         "WIPRO.BO":        507685,\
                         "YESBANK.BO":      532648})

def get_beta_for_ticker(ticker):
    try:
        url = 'https://in.finance.yahoo.com/quote/' + ticker + '?p=' + ticker + '&.tsrc=fin-srch'
        page = requests.get(url)
        page_content = page.content
        soup = BeautifulSoup(page_content, "lxml")
        tabl = soup.find("table", {"class": "W(100%) M(0) Bdcl(c)"})
        print("Table: ", tabl.text)
        rows = tabl.find_all("tr")
        row = rows[1]
        t_string = str(row)
        pos_trsdu = t_string.find("Trsdu(0.3s)")
        if (pos_trsdu != -1):
            pos_span = t_string.find("</span>", pos_trsdu, len(t_string))
            temp = t_string[pos_trsdu :pos_span]
            pos = temp.find(">")
            beta = temp[pos + 1 : len(temp)]
            return beta
        
        return -1
    except:
        print("Problem scraping beta data for ", ticker)

def get_historical_revenue_for_ticker(ticker_id):
    try:
        url = 'http://financials.morningstar.com/income-statement/is.html?t=' + str(ticker_id) + '&region=ind&culture=en-US&platform=sal'
        print("URL: ", url)
        page = requests.get(url)
        page_content = page.content
        soup = BeautifulSoup(page_content, 'html.parser')
        print("Content: ", page_content)
        tabl = soup.find_all("div", {"class": "main main10 "})
        print("Table: ", tabl)
    except:
        print("Problem scraping revenue data for ", ticker)

beta_list = []    
tickers_temp = ["BAJFINANCE.BO"]
for ticker in tickers_temp:
    beta_ticker = get_beta_for_ticker(ticker)
    print("Beta: ", beta_ticker)
    beta_list.append(beta_ticker)

# Now collate the data
list_of_tuples = list(zip(tickers_temp, beta_list))
ticker_data = pd.DataFrame(list_of_tuples, columns = ['Ticker', 'Beta'])
get_historical_revenue_for_ticker(ticker_symbol_id['BAJFINANCE.BO'])
 
    
