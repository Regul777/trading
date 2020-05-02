#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 01:02:51 2020

@author: nishant.gupta
"""

from selenium_driver import selenium_driver
from utils import string_util

class cash_flow_statement_getter:
    def __init__(self, url):
        self.url = url
        self.free_cash_flow = []
        self.cash_from_operating_activities = []
        self.cash_used_for_investing_activities = []
        self.cash_used_for_financial_activities = []
    
    def get_data(self):
        free_cash_flow_xtag = '//*[@id="data_i97"]'
        cash_oper_activities_xtag = '//*[@id="data_tts1"]'
        cash_investing_activities_xtag = '//*[@id="data_tts2"]'
        cash_financial_activities_xtag = '//*[@id="data_tts3"]'
        
        # Now get the data from the url
        driver = selenium_driver(url = self.url, num_retries = 5)
        self.free_cash_flow = string_util.get_processed_data(driver.find_xpath(element_xpath = free_cash_flow_xtag))
        print("Free cash flow: ", self.free_cash_flow)
        self.cash_used_for_investing_activities = string_util.get_processed_data(driver.find_xpath(element_xpath = cash_investing_activities_xtag))
        print("Cash for investing activities: ", self.cash_used_for_investing_activities)
        self.cash_used_for_financial_activities = string_util.get_processed_data(driver.find_xpath(element_xpath = cash_financial_activities_xtag))
        print("Cash for financial activities: ", self.cash_used_for_financial_activities)
        self.cash_from_operating_activities = string_util.get_processed_data(driver.find_xpath(element_xpath = cash_oper_activities_xtag))
        print("Cash from operating activities: ", self.cash_from_operating_activities)
        
url = 'http://financials.morningstar.com/cash-flow/cf.html?t=500209&region=ind&culture=en-US&platform=sal'
income_statement = cash_flow_statement_getter(url = url)
income_statement.get_data()
        