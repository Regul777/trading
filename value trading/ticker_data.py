#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 00:02:02 2020

@author: nishant.gupta
"""

import numpy as np
import pandas as pd
import requests

from balance_sheet  import balance_sheet_data_getter
from bs4 import BeautifulSoup
from cash_flow_statement import cash_flow_statement_getter
from common import ticker_symbol_id
from income_statement import income_statement_getter
from selenium_driver import selenium_driver
from utils import string_util

# SBI FD gives a return of 6.5%
risk_free_return_rate = 6.5

# Sensex has goven a CAGR of 17.1% from 1979-2019. However, to be on a conservative side we are considering it as 15%
market_return_rate = 15

class collated_data:
    def __init__(self, beta, ticker_data, avg_net_margin = 0, avg_fcf_net_income_ratio = 0, \
                 Wd = 0 , Rd = 0, t = 0, We = 0, Re = 0, wacc = 0, dcf = 0, current_ratio = 0,\
                 intrinsic_value = 0, market_value = 0):
        # Wd = Weight of debt
        # Rd = Rate of debt
        # We = Weight of equity
        # Re = Rate of equity (CAPM) Note that this is different from ROE
        self.beta = beta
        self.ticker_data = ticker_data
        self.avg_net_margin = avg_net_margin
        self.avg_fcf_net_income_ratio = avg_fcf_net_income_ratio
        self.Wd = Wd
        self.Rd = Rd
        self.t = t
        self.We = We
        self.Re = Re
        self.wacc = wacc
        self.dcf = dcf
        self.current_ratio = current_ratio
        self.intrinsic_value = intrinsic_value
        self.market_value = market_value
        
class ticker_data_getter:
    def get_additional_ticker_data_from_moneycontrol(ticker):
        eps = 0.0
        pe = 0.0
        industry_pe = 0.0
        book_value = 0.0
        try:
            ticker_id = ticker_symbol_id[ticker]
            url = 'https://www.moneycontrol.com/stocksmarketsindia/'
            driver = selenium_driver(url = url, num_retries = 5)
            search_box_xpath = '//*[@id="search_str"]'
            search_click_xpath = '/html/body/header/div[1]/div/div[2]/div[2]/div[1]/a'
            eps_xpath = '//*[@id="standalone_valuation"]/ul/li[2]/ul/li[3]/div[2]'
            pe_xpath = '//*[@id="standalone_valuation"]/ul/li[1]/ul/li[2]/div[2]'
            industry_pe_xpath = '//*[@id="standalone_valuation"]/ul/li[2]/ul/li[2]/div[2]'
            book_value_xpath = '//*[@id="standalone_valuation"]/ul/li[1]/ul/li[3]/div[2]'
            content_eps = driver.get_element_by_searching(search_box_xpath = search_box_xpath,\
                                                  element_key = ticker_id,\
                                                  search_box_click_xpath = search_click_xpath,\
                                                  element_xpath = eps_xpath)
            print("EPS: ", content_eps)
            eps = string_util.get_processed_data(content_eps)[0]
            content_pe = driver.get_element_by_searching(search_box_xpath = search_box_xpath,\
                                                  element_key = ticker_id,\
                                                  search_box_click_xpath = search_click_xpath,\
                                                  element_xpath = pe_xpath)
            print("P/E: ", content_pe)
            pe = string_util.get_processed_data(content_pe)[0]
            content_industry_pe = driver.get_element_by_searching(search_box_xpath = search_box_xpath,\
                                                  element_key = ticker_id,\
                                                  search_box_click_xpath = search_click_xpath,\
                                                  element_xpath = industry_pe_xpath)
            print("IP/E: ", content_industry_pe)
            industry_pe = string_util.get_processed_data(content_industry_pe)[0]
            content_bv = driver.get_element_by_searching(search_box_xpath = search_box_xpath,\
                                                  element_key = ticker_id,\
                                                  search_box_click_xpath = search_click_xpath,\
                                                  element_xpath = book_value_xpath)
            print("BV: ", content_bv)
            book_value = string_util.get_processed_data(content_bv)[0]
        except Exception as e:
            print("Encountered exception: ", e)
            print("Encountered some error while fetching additional data for: ", ticker, " from moneycontrol")
        
        # TODO: Make a struct for the additional data too 
        return eps, pe, industry_pe, book_value
            
    def get_beta_for_ticker(ticker):
        beta = 0.0
        try:
            ticker_id = ticker_symbol_id[ticker]
            url = 'https://www.moneycontrol.com/stocksmarketsindia/'
            driver = selenium_driver(url = url, num_retries = 5)
            search_box_xpath = '//*[@id="search_str"]'
            search_click_xpath = '/html/body/header/div[1]/div/div[2]/div[2]/div[1]/a'
            content = driver.get_content_by_searching(search_box_xpath = search_box_xpath,\
                                                      element_key = ticker_id,\
                                                      search_box_click_xpath = search_click_xpath)
            soup = BeautifulSoup(content, "lxml")
            tabl = soup.find("div", {"class": "bsedata_bx"})
            temp = tabl.find_all("div", {"class" : "disin vt"})
            beta_str = temp[1].text
            beta_str = beta_str.replace('\n', '')
            beta_str = beta_str.replace(' ', '')
            beta = float(beta_str[5: len(beta_str)])
        except:
            print("Encountered some error while fetching beta for: ", ticker, " from moneycontrol.")
        
        return beta

    def get_beta_for_ticker_yahoo_finance(ticker):
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
    
    def get_market_price(ticker):
        try:
            url = 'https://in.finance.yahoo.com/quote/' + ticker + '?p=' + ticker + '&.tsrc=fin-srch'
            driver = selenium_driver(url = url, num_retries = 5)
            price = string_util.get_processed_data(driver.find_xpath(element_xpath = '//*[@id="quote-header-info"]/div[3]/div/div/span[1]'))[0]
            return price
        except:
            print("Problem scraping market price for ", ticker)
            
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
        except Exception as e:
            print("Encountered exception: ", e)
            print("Problem in scraping financial data for ", ticker)
            

    def get_data_for_all_tickers_all_financial_statements(all_tickers):
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
                    balance_sheet.common_stock.insert(0, "Common stock")
        
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
                        st_debt = ["Short term debt", "0", "0", "0", "0", "0"]
                    
                    print("Short Term debt: ", st_debt)
                    lt_debt = []
                    if (len(balance_sheet.long_term_debt) > 0):
                        balance_sheet.long_term_debt.insert(0, "Long term debt")
                        lt_debt = balance_sheet.long_term_debt
                    else:
                        lt_debt = ["Long term debt", "0", "0", "0", "0", "0"]
        
                    print("Long term debt: ", lt_debt)
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
                                           balance_sheet.common_stock,\
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
    
    def get_data_for_all_tickers(tickers):
        # This API adds other parameters to the data we got from financial statements
        # This will be used to compute future cash flow and other futuristic data
        tickers_data_from_all_statements = ticker_data_getter.get_data_for_all_tickers_all_financial_statements(tickers)
        
        collated_data_dict = {}
        # First add slope to all the fields in "ticker_data" to get the trend of all the metrics
        for ticker in tickers_data_from_all_statements.keys():
            try:
                beta = tickers_data_from_all_statements[ticker].beta
                ticker_data = tickers_data_from_all_statements[ticker].ticker_data
            
                # Calculate the net income margin as Net income / Revenue 
                ticker_data_temp = ticker_data.transpose()
                ticker_data_temp['Net income Margin'] = ticker_data_temp['Net income'] / ticker_data_temp['Revenue']
                ticker_data_temp['FCF / Net income'] = ticker_data_temp['Free cash flow'] / ticker_data_temp['Net income']
                # Now calculate the average net income margin for these 5 years
                margin_data = ticker_data_temp['Net income Margin']
                average_net_income_margin_ticker = np.mean(margin_data)
                print("Average net margin: ", average_net_income_margin_ticker)
                
                # calculate average_free_cash_flow / net income ratio for these 5 years
                free_cash_flow_to_net_income_data = ticker_data_temp['FCF / Net income']
                average_free_cash_flow_to_net_income = np.mean(free_cash_flow_to_net_income_data)
                print("Average fcf/net income: ", average_free_cash_flow_to_net_income)
                
                ticker_data = ticker_data_temp.transpose()            
                collated_data_dict[ticker] = collated_data(beta = beta,\
                                                           ticker_data = ticker_data,\
                                                           avg_net_margin = average_net_income_margin_ticker,\
                                                           avg_fcf_net_income_ratio = average_free_cash_flow_to_net_income)
            except:
                print("Encountered error while getting data for ticker: ", ticker)
        return collated_data_dict
    
    def get_data_for_value_investing(tickers):
        # This API calculates projected future cash flow and WACC
        collated_data_dict = {}
        tickers_collated_data = ticker_data_getter.get_data_for_all_tickers(tickers)
        for ticker in tickers_collated_data.keys():
            try:
                average_net_income_margin = tickers_collated_data[ticker].avg_net_margin
                avg_fcf_net_income_ratio = tickers_collated_data[ticker].avg_fcf_net_income_ratio
                ticker_data = tickers_collated_data[ticker].ticker_data
                ticker_data_temp = ticker_data.transpose()
                # TODO: Remove the following hard coding 4 -> Revenue of Y5
                starting_revenue = ticker_data_temp['Revenue'][0]
                latest_revenue = ticker_data_temp['Revenue'][4]
                # TODO: Remove following hard codings for Y5 and number of years = 5
                revenue_growth_rate = np.exp((np.log(latest_revenue) - np.log(starting_revenue)) / 5) - 1
                future_net_income = []
                for i in range(1, 6):
                    net_income_for_this_year = latest_revenue * average_net_income_margin
                    latest_revenue = latest_revenue * (1 + revenue_growth_rate)
                    future_net_income.append(net_income_for_this_year)
                ticker_data_temp['Future Net income'] = future_net_income
                
                future_cash_flow = []
                for i in range(1, 6):
                    future_cash_flow.append(future_net_income[i-1] * avg_fcf_net_income_ratio)
                ticker_data_temp['Future cash flow'] = future_cash_flow
                
                # Get all the data to calculate the WACC
                # explicitly casting the st debt and lt debt to float coz. for some cases where the values
                # are still the string
                st_debt = float(ticker_data_temp['Short term debt'][4])
                lt_debt = float(ticker_data_temp['Long term debt'][4])
                common_stk = ticker_data_temp['Common stock'][4]
                interest_expense = ticker_data_temp['Income interest'][4]
                income_taxes = ticker_data_temp['Provision taxes'][4]
                income_before_taxes = ticker_data_temp['Income before taxes'][4]
                
                # Calculating current ratio now
                current_assets = ticker_data_temp['Current Assets'][4]
                print("CA: ", current_assets)
                total_liabilities = ticker_data_temp['Total liabilites'][4]
                print("TCL: ", total_liabilities)
                current_ratio = current_assets / total_liabilities
                
                # TODO: Market rate is latest but financial data may be from previous year
                # so, market_cap caluclated below may contain stale data and hence WACC may get effected
                market_rate = ticker_data_getter.get_market_price(ticker)
                market_cap = common_stk * market_rate
                total_debt = st_debt + lt_debt
                We = market_cap / (market_cap + total_debt)
                Wd = total_debt / (market_cap + total_debt)
                Rd = 0
                if (total_debt != 0) :
                    Rd = interest_expense / total_debt
                t = income_taxes / income_before_taxes
                # Calculating the Re in CAPM equation
                # Note that this is different from ROE explianed here 
                # https://www.quora.com/Whats-the-difference-between-return-on-equity-and-cost-of-equity
                Re = (risk_free_return_rate + float(tickers_collated_data[ticker].beta) * \
                    (market_return_rate - risk_free_return_rate)) / 100
                
                wacc = (Rd * Wd * (1-t)) + (Re * We)
                ticker_data = ticker_data_temp.transpose()
                # TODO: Remove following hard codings for Y5 and number of years = 5
                # ticker_data['Slope'] = np.exp((np.log(ticker_data['Y5'].tolist()) - np.log(ticker_data['Y1'].tolist())) / 5) - 1
                
                collated_data_dict[ticker] = collated_data(beta = tickers_collated_data[ticker].beta,\
                                                           ticker_data = ticker_data,\
                                                           avg_net_margin = average_net_income_margin,\
                                                           avg_fcf_net_income_ratio = avg_fcf_net_income_ratio,
                                                           Wd = Wd, Rd = Rd, t = t, We = We, Re = Re,\
                                                           wacc = wacc,\
                                                           current_ratio = current_ratio,\
                                                           market_value = market_rate)
            except:
                print("Error encountered while calculating values for value investing for: ", ticker)
        return collated_data_dict
    
    def get_intrinsic_value_of_tickers(tickers):
        # This API calculates the intrinsic value of the stock by using Discounted cash flow model
        collated_data_dict = {}
        # Following suggests perpetual growth rate of 7.5% in indian markets
        # https://www.grantthornton.in/globalassets/1.-member-firms/india/assets/pdfs/grant_thornton-valuation_insights-october_2015.pdf
        # Assuming 6% for this is a bit conservative and that's fine
        perpetual_growth_rate = 0.06
        tickers_collated_data = ticker_data_getter.get_data_for_value_investing(tickers)
        for ticker in tickers_collated_data.keys():
            try:
                ticker_data = tickers_collated_data[ticker].ticker_data
                wacc_ticker = tickers_collated_data[ticker].wacc
                ticker_data_temp = ticker_data.transpose()
                fcf_data_ticker = ticker_data_temp['Future cash flow'].tolist()
                discounted_cash_flow = 0
                
                # TODO: Remove the hardcoding around final year below
                final_year_fcf = fcf_data_ticker[4]
                for i in range(len(fcf_data_ticker)):
                    fcf = fcf_data_ticker[i]
                    discounted_cash_flow = discounted_cash_flow + (fcf / ((1 + wacc_ticker) ** i))
                print("DCF: ", discounted_cash_flow)
                terminal_value = final_year_fcf * (1 + perpetual_growth_rate) / (wacc_ticker - perpetual_growth_rate)
                discounted_cash_flow += terminal_value
                print("Terminal value: ", terminal_value)
                
                common_stk = ticker_data_temp['Common stock'][4]
                intrinsic_value = discounted_cash_flow / common_stk
                collated_data = tickers_collated_data[ticker]
                collated_data.dcf = discounted_cash_flow
                collated_data.intrinsic_value = intrinsic_value
                collated_data_dict[ticker] = collated_data
            except:
                print("Error while calculating instrinsic value of the ticker: ", ticker)
        return collated_data_dict
                
#tickers_temp = ["INFY.BO"]
#ticker = "SAIL.BO"
#eps, pe, industry_pe, book_value = ticker_data_getter.get_additional_ticker_data_from_moneycontrol(ticker)
#tickers_collated_data = ticker_data_getter.get_intrinsic_value_of_tickers(tickers_temp)
# Now collate the data
#list_of_tuples = list(zip(tickers_temp, beta_list))
#ticker_data = pd.DataFrame(list_of_tuples, columns = ['Ticker', 'Beta'])
#get_historical_revenue_for_ticker(ticker_symbol_id['BAJFINANCE.BO'])
 
    
