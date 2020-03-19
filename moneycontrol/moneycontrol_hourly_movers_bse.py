#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 23:00:13 2020

@author: nishant.gupta
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_hourly_movers(url, num_stocks) :
  page = requests.get(url)
  page_content = page.content
  soup = BeautifulSoup(page_content, "lxml")
  table = soup.find_all("div", {"class" : "bsr_table bsr_table930 hist_tbl"})

  # output
  # schema is: 
  # Name, Open price, Close price, Gain, %Gain, Current price
  ctr = 0
  output = []

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
      soup2 = BeautifulSoup(str(span_section), "lxml")
      all_links = soup2.find_all("a")
      redirect_url = all_links[0]['href']
      redirect_page = requests.get(redirect_url)
      redirect_content = redirect_page.content
      soup3 = BeautifulSoup(redirect_content, "lxml")
      prev_close_table = soup3.find_all("p", {"class" : "prev_open priceprevclose"})
      prev_close_val = prev_close_table[0].text
      table_redirect = soup3.find_all("div", {"class" : "bsedata_bx"})
      for t_redirect in table_redirect:
          rows_redirect_fifty_two_weeks = t_redirect.find_all("div", {"class" : "clearfix lowhigh_band week52_lowhigh_wrap"})
          soup4 = BeautifulSoup(str(rows_redirect_fifty_two_weeks), "lxml")         
          low_segment_year = soup4.find_all("div", {"class" : "low_high1"})
          fifty_two_week_low = low_segment_year[0].text
          high_segment_year = soup4.find_all("div", {"class" : "low_high3"})
          fifty_two_week_high = high_segment_year[0].text
          
          # Do the exact same thing for today data
          # TODO: Create a function for low_high1 and low_high3 and use it in this for loop
          # TODO: See if we can have a generic which takes the segment name, type and return the required field 
          rows_redirect_today = t_redirect.find_all("div", {"class" : "clearfix lowhigh_band todays_lowhigh_wrap"})
          soup5 = BeautifulSoup(str(rows_redirect_today), "lxml")
          low_segment_today = soup5.find_all("div", {"class" : "low_high1"})
          today_low = low_segment_today[0].text
          high_segment_today = soup5.find_all("div", {"class" : "low_high3"})
          today_high = high_segment_today[0].text
          

      cols = [x.text.strip() for x in cols]
      name = cols[0].split('\n')[0]
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
        
      output.append(row_data)
      ctr += 1
      if (ctr > num_stocks):
        break
    
  return output

hourly_gain_url = 'https://www.moneycontrol.com/stocks/marketstats/hourly_gain/bse/curr_hour/index.php'
hourly_loss_url = 'https://www.moneycontrol.com/stocks/marketstats/hourly_loss/bse/curr_hour/index.php'
num_stocks = 5

hourly_gainers = get_hourly_movers(hourly_gain_url, num_stocks)
hourly_losers = get_hourly_movers(hourly_loss_url, num_stocks)

#TODO: Create a generic schema for this file and use it both for gainers and losers
hourly_gainers = pd.DataFrame(hourly_gainers, columns=['Name', 'Prev Close', 'Open Price', 'Close Price', 'Gain', 'Gain %', 'Current Price', '52Week low', '52Week high', 'Today low', 'Today high'])
hourly_losers = pd.DataFrame(hourly_losers, columns=['Name', 'Prev Close', 'Open Price', 'Close Price', 'Gain', 'Gain %', 'Current Price', '52Week low', '52Week high', 'Today low', 'Today high'])

print(hourly_gainers)
print(hourly_losers)