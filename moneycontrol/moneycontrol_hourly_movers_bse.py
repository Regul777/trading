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
  num_stocks = 20
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
      cols = [x.text.strip() for x in cols]        
      name = cols[0].split('\n')[0]
      row_data.append(name)
      row_data.append(cols[1])
      row_data.append(cols[2])
      row_data.append(cols[3])
      row_data.append(cols[4])
      row_data.append(cols[5])
        
      output.append(row_data)
      ctr += 1
      if (ctr > num_stocks):
        break
    
  return output

hourly_gain_url = 'https://www.moneycontrol.com/stocks/marketstats/hourly_gain/bse/curr_hour/index.php'
hourly_loss_url = 'https://www.moneycontrol.com/stocks/marketstats/hourly_loss/bse/curr_hour/index.php'
num_stocks = 10

hourly_gainers = get_hourly_movers(hourly_gain_url, num_stocks)
hourly_losers = get_hourly_movers(hourly_loss_url, num_stocks)
hourly_gainers = pd.DataFrame(hourly_gainers, columns=['Name', 'Open Price', 'Close Price', 'Gain', 'Gain %', 'Current Price'])
hourly_losers = pd.DataFrame(hourly_losers, columns=['Name', 'Open Price', 'Close Price', 'Gain', 'Gain %', 'Current Price'])