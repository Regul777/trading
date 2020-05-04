#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 00:02:02 2020

@author: nishant.gupta
"""

import pandas as pd
import requests

from balance_sheet  import balance_sheet_data_getter
from bs4 import BeautifulSoup
from cash_flow_statement import cash_flow_statement_getter
from income_statement import income_statement_getter

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

class collated_data:
    def __init__(self, beta, ticker_data):
        self.beta = beta
        self.ticker_data = ticker_data
        
class ticker_data_getter:
    def get_beta_for_ticker(ticker):
        try:
            url = 'https://in.finance.yahoo.com/quote/' + ticker + '?p=' + ticker + '&.tsrc=fin-srch'
            page = requests.get(url)
            page_content = page.content
            soup = BeautifulSoup(page_content, "lxml")
            tabl = soup.find("table", {"class": "W(100%) M(0) Bdcl(c)"})
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
            
    def financial_data_from_morning_star(ticker):
        try:
            ticker_id = ticker_symbol_id[ticker]
            balance_sheet_url = 'http://financials.morningstar.com/balance-sheet/bs.html?t=' + str(ticker_id) + \
                                '&region=ind&culture=en-US&platform=sal'
            balance_sheet = balance_sheet_data_getter(balance_sheet_url)
            balance_sheet.get_data()
            
            income_statement_url = 'https://financials.morningstar.com/income-statement/is.html?t=' + str(ticker_id) + \
                                   '&region=ind&culture=en-US&platform=sal'
            income_statement = income_statement_getter(income_statement_url)
            income_statement.get_data()
            
            cash_flow_url = 'http://financials.morningstar.com/cash-flow/cf.html?t=' + str(ticker_id) + \
                            '&region=ind&culture=en-US&platform=sal'
            cash_flow_statement = cash_flow_statement_getter(cash_flow_url)
            cash_flow_statement.get_data()
            
            return balance_sheet, income_statement, cash_flow_statement
        except:
            print("Problem in scraping financial data for ", ticker)
            

    def get_data_for_all_tickers(all_tickers):
        Years = ["Data", "Y1", "Y2", "Y3", "Y4", "Y5"]
        tickers = all_tickers
        collated_data_dict = {}
        while (len(tickers) > 0):
            try:
                for ticker in tickers:
                    beta_ticker = ticker_data_getter.get_beta_for_ticker(ticker)
                    print("Beta: ", beta_ticker)
                    financial_data_ticker = ticker_data_getter.financial_data_from_morning_star(ticker)
                    balance_sheet = financial_data_ticker[0]
                    balance_sheet.total_current_assets.insert(0, "Current Assets")
                    balance_sheet.total_current_liabilities.insert(0, "Current Liabilities")
                    balance_sheet.total_liabilities.insert(0, "Total liabilites")
                    balance_sheet.total_stockholders_equity.insert(0, "Stock holder's equity")
        
                    income_statement = financial_data_ticker[1]
                    income_statement.revenue.insert(0, "Revenue")
                    income_statement.net_income.insert(0, "Net income")
                    income_statement.income_before_taxes.insert(0, "Income before taxes")
                    income_statement.provision_taxes.insert(0, "Provision taxes")
        
                    cash_flow_statement = financial_data_ticker[2]
                    cash_flow_statement.free_cash_flow.insert(0, "Free cash flow")
                    cash_flow_statement.cash_from_operating_activities.insert(0, "Cash from operating activities")
                    cash_flow_statement.cash_used_for_investing_activities.insert(0, "Cash used for investing activities")
                    cash_flow_statement.cash_used_for_financial_activities.insert(0, "Cash for financial activities")
        
                    st_debt = []
                    if (len(balance_sheet.short_term_debt) > 0):
                        balance_sheet.short_term_debt.insert(0, "Short term debt")
                        st_debt = balance_sheet.short_term_debt
                    else:
                        st_debt = ["Short term debt", "-", "-", "-", "-", "-"]
        
                    lt_debt = []
                    if (len(balance_sheet.long_term_debt) > 0):
                        balance_sheet.long_term_debt.insert(0, "Long term debt")
                        lt_debt = balance_sheet.long_term_debt
                    else:
                        lt_debt = ["Long term debt", "-", "-", "-", "-", "-"]
        
                    income_interest = []
                    if (len(income_statement.income_interest) > 0):
                        income_statement.income_interest.insert(0, "Income interest")
                        income_interest = income_statement.income_interest
                    else:
                        income_interest = ["Income interest", "-", "-", "-", "-", "-"]
     
                    list_tuples = list(zip(balance_sheet.total_current_assets,\
                                           balance_sheet.total_current_liabilities,\
                                           balance_sheet.total_liabilities,\
                                           balance_sheet.total_stockholders_equity,\
                                           income_statement.revenue,\
                                           income_statement.net_income,\
                                           income_statement.income_before_taxes,\
                                           income_statement.provision_taxes,\
                                           cash_flow_statement.free_cash_flow,\
                                           cash_flow_statement.cash_from_operating_activities,\
                                           cash_flow_statement.cash_used_for_investing_activities,\
                                           cash_flow_statement.cash_used_for_financial_activities,\
                                           st_debt,\
                                           lt_debt,\
                                           income_interest))
    
                    ticker_data_temp = pd.DataFrame(list_tuples)
                    ticker_data = ticker_data_temp.transpose()
                    ticker_data.columns = Years
                    ticker_data.set_index("Data", inplace = True)
                    collated_data_dict[ticker] = collated_data(beta = beta_ticker,\
                                                               ticker_data = ticker_data)
                    tickers.remove(ticker)
            except:
                print("Encountered some error while fetching data for ticker: ", ticker)
                tickers.remove(ticker)

        return collated_data_dict
        
# tickers_temp = ["INFY.BO", "BAJFINANCE.BO", "NESTLEIND.BO"]
tickers_collated_data = ticker_data_getter.get_data_for_all_tickers(tickers)

# Now collate the data
#list_of_tuples = list(zip(tickers_temp, beta_list))
#ticker_data = pd.DataFrame(list_of_tuples, columns = ['Ticker', 'Beta'])
#get_historical_revenue_for_ticker(ticker_symbol_id['BAJFINANCE.BO'])
 
    
