#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 00:26:02 2020

@author: nishant.gupta
"""

from selenium_driver import selenium_driver
from utils import string_util

class income_statement_getter:
    def __init__(self, url):
        self.url = url
        self.revenue = []
        self.net_income = []
        self.income_before_taxes = []
        self.provision_taxes = []
        self.income_interest = []
    
    def get_data(self):
        revenue_xtag = '//*[@id="data_i1"]'
        net_income_xtag = '//*[@id="data_i80"]'
        income_before_tax_xtag = '//*[@id="data_i60"]'
        provision_taxes_xtag = '//*[@id="data_i61"]'
        income_interest_string = "//div[contains(text(),'Interest Expense')]"
        income_interest_xtag = '//*[@id="data_i51"]'
        
        # Now get the data from the url
        driver = selenium_driver(url = self.url, num_retries = 5)
        self.revenue = string_util.get_processed_data(driver.find_xpath(element_xpath = revenue_xtag))
        print("Revenue : ", self.revenue)
        self.net_income = string_util.get_processed_data(driver.find_xpath(element_xpath = net_income_xtag))
        print("Net income: ", self.net_income)
        self.income_before_taxes = string_util.get_processed_data(driver.find_xpath(element_xpath = income_before_tax_xtag))
        self.provision_taxes = string_util.get_processed_data(driver.find_xpath(element_xpath = provision_taxes_xtag))
        print("Provision taxes: ", self.provision_taxes)
        income_interest_present = driver.find_xpath(element_xpath = income_interest_string)
        if (income_interest_present == ""):
            print("No interest data found.. possibly because company had no debt")
        else:
            self.income_interest = string_util.get_processed_data(driver.find_xpath(element_xpath = income_interest_xtag))
            print("Income interest: ", self.income_interest)

url = 'https://financials.morningstar.com/income-statement/is.html?t=500034&region=ind&culture=en-US&platform=sal'
income_statement = income_statement_getter(url = url)
income_statement.get_data()