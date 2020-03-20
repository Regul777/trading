#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 23:00:13 2020

@author: nishant.gupta
"""

from bs4 import BeautifulSoup
from yahoo_finance_data_getter import yahoo_finance_data_getter
import pandas as pd
import requests


class moneycontrol_data_extractor:

  @staticmethod
  def get_redirect_url(span_section) :
    soup = BeautifulSoup(str(span_section), "lxml")
    all_links = soup.find_all("a")
    redirect_url = all_links[0]['href']
    return redirect_url

  @staticmethod
  def get_low_high(rows_redirect) :
    soup = BeautifulSoup(str(rows_redirect), "lxml")
    low_segment = soup.find_all("div", {"class" : "low_high1"})
    low = low_segment[0].text
    high_segment = soup.find_all("div", {"class" : "low_high3"})
    high = high_segment[0].text
    return low, high
  
  @staticmethod
  def get_today_high_low(redirect_content) :
    soup = BeautifulSoup(redirect_content, "lxml")
    table_redirect = soup.find_all("div", {"class" : "bsedata_bx"})
    for t_redirect in table_redirect:
      rows_redirect_today = t_redirect.find_all("div", {"class" : "clearfix lowhigh_band todays_lowhigh_wrap"})
      low, high = moneycontrol_data_extractor.get_low_high(rows_redirect_today)
      return low, high

  @staticmethod
  def get_symbol_for_interesting_stock(content) :
    soup = BeautifulSoup(content, "lxml")
    inputs = soup.select('input[id=nseid]')
    print("input: ", input)
    
    # There is only a single entry of this tag on the page
    return inputs[0]['value']
        
  @staticmethod
  def get_fifty_two_week_high_low(redirect_content) :
    soup = BeautifulSoup(redirect_content, "lxml")
    table_redirect = soup.find_all("div", {"class" : "bsedata_bx"})
    for t_redirect in table_redirect:
      rows_redirect_fifty_two_weeks = t_redirect.find_all("div", {"class" : "clearfix lowhigh_band week52_lowhigh_wrap"})
      low, high = moneycontrol_data_extractor.get_low_high(rows_redirect_fifty_two_weeks)
      return low,high
  
  @staticmethod
  def get_moving_averages(redirect_content) :
    moving_averages = []
    soup = BeautifulSoup(redirect_content, "lxml")
    table = soup.find_all("div", {"class" : "techany smaD"})
    rows = table[0].tbody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [x.text.strip() for x in cols]
        ma = []
        ma.append(cols[0])
        ma.append(cols[1])
        moving_averages.append(ma)
    return moving_averages
      
    
  @staticmethod
  def get_hourly_movers(url, num_stocks, num_days_for_moving_average) :
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, "lxml")
    table = soup.find_all("div", {"class" : "bsr_table bsr_table930 hist_tbl"})

    # output
    # schema is: 
    # Name, Open price, Close price, Gain, %Gain, Current price
    ctr = 0
    output = []
    place_of_moving_average = []
    place_of_moving_average = {5 : 0, 10 : 1, 20 : 2, 50 : 3, 200 : 4}
    moving_avg_idx = place_of_moving_average[num_days_for_moving_average]
    
    # Presently we have only one table with above name so, we will be having
    # only one entry in the table list, but just for the sake of safety we are
    # still assuming it a list and proceeding
    for t in table:
      rows = t.tbody.find_all('tr')
      for row in rows:
        row_data = []
        cols = row.find_all('td')
        fifty_two_week_low = 0
        fifty_two_week_high = 0
        today_low = 0
        today_high = 0
        span_section = row.find_all("span", {"class" : "gld13 disin"})
        redirect_url = moneycontrol_data_extractor.get_redirect_url(span_section)
        redirect_page = requests.get(redirect_url)
        redirect_content = redirect_page.content
        
        # Schema of moving averages returned by below API is:
        # 5    82.44
        # 10	85.94
        # 20	95.08
        # 50	106.87
        # 100	110.20
        # 200	119.69
        moving_averages = moneycontrol_data_extractor.get_moving_averages(redirect_content)
        
        # Following comment out code is pretty unreliable as symbols are only available
        # for stocks which are listed on BSE and without symbols we can not use yahoo financials
        # So, for now we are going ahead with "SIMPLE MOVING AVERAGES" on the redirect url     
        # symbol = moneycontrol_data_extractor.get_symbol_for_interesting_stock(redirect_content)
        # symbol += ".BO"
        # mean_data = 0
        # if (symbol == ".BO") :
        #   print("Could not fetch symbol. Possible readon: this is not listed in NSE yet.")
        # else :
        #   mean_data = yahoo_finance_data_getter.get_mean_data_for_ticker(symbol , 50)
        
        soup = BeautifulSoup(redirect_content, "lxml")
        prev_close_table = soup.find_all("p", {"class" : "prev_open priceprevclose"})
        prev_close_val = prev_close_table[0].text
        fifty_two_week_low, fifty_two_week_high = moneycontrol_data_extractor.get_fifty_two_week_high_low(redirect_content)
        today_low, today_high = moneycontrol_data_extractor.get_today_high_low(redirect_content)          
        cols = [x.text.strip() for x in cols]
        name = cols[0].split('\n')[0]
      
        # We have got all the data now, fill it in the schema
        row_data.append(name)
        row_data.append(prev_close_val)
        row_data.append(cols[1])
        row_data.append(cols[2])
        row_data.append(cols[3])
        row_data.append(cols[4])
        row_data.append(cols[5])
        row_data.append(fifty_two_week_low)
        row_data.append(fifty_two_week_high)
        row_data.append(today_low)
        row_data.append(today_high)
        row_data.append(moving_averages[0][1])
        row_data.append(moving_averages[1][1])
        row_data.append(moving_averages[2][1])
        row_data.append(moving_averages[3][1])
        row_data.append(moving_averages[4][1])
        
        # Setup an alert when stock breaches it's MA
        signal = 'B'
        if (cols[5] < moving_averages[moving_avg_idx][1]) :
            print("Stock : ", name , " has gone below the : ", num_days_for_moving_average, " days moving average")
        else :
            print("Stock : ", name, " has gone past the moving average")
            signal = 'S'            
        
        row_data.append(signal)
        output.append(row_data)
        ctr += 1
        if (ctr > num_stocks):
          break
    
    return output

hourly_gain_url = 'https://www.moneycontrol.com/stocks/marketstats/hourly_gain/bse/curr_hour/index.php'
hourly_loss_url = 'https://www.moneycontrol.com/stocks/marketstats/hourly_loss/bse/curr_hour/index.php'
num_stocks = 10
moving_average_to_consider = 200
hourly_gainers = moneycontrol_data_extractor.get_hourly_movers(hourly_gain_url, num_stocks, moving_average_to_consider)
hourly_losers = moneycontrol_data_extractor.get_hourly_movers(hourly_loss_url, num_stocks, moving_average_to_consider)

schema = ['Name', 'Prev Close', 'Open Price', 'Close Price', 'Gain', 'Gain %', 'Current Price', '52Week low', '52Week high', 'Today low', 'Today high', '5 MA', '10 MA', '20 MA', '50 MA', '200 MA', 'Signal']
hourly_gainers = pd.DataFrame(hourly_gainers, columns = schema)
hourly_losers = pd.DataFrame(hourly_losers, columns = schema)

print(hourly_gainers)
print(hourly_losers)