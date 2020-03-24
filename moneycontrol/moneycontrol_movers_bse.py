#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 23:00:13 2020

@author: nishant.gupta
"""

from bs4 import BeautifulSoup
from yahoo_finance_data_getter import yahoo_finance_data_getter
import requests

class packed_data_today :
    def __init__(self, low, high, fifty_two_week_low, fifty_two_week_high, open_price, close_price, gain, gain_percent, volume) :
      self.low = low
      self.high = high
      self.fifty_two_week_low = fifty_two_week_low        
      self.fifty_two_week_high = fifty_two_week_high
      self.open_price = open_price
      self.close_price = close_price
      self.gain = gain
      self.gain_percent = gain_percent
      self.volume = volume

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
  def get_today_open_close_gain_volume(redirect_content) :
    soup = BeautifulSoup(redirect_content, "lxml")
    open_price_table = soup.find_all("p", {"class" : "prev_open priceopen"})
    open_price = open_price_table[0].text
    close_price = soup.find_all("span", {"class" : "txt15B bse_span_price_wrap"})
    close_price = close_price[0].text
    volume = soup.find_all("span", {"class" : "txt13_pc volume_data"})
    volume = volume[0].text
    gain_data = soup.find_all("span", {"class" : "bse_span_price_change_prcnt txt14G"})
    
    #If we don't have any gain data for this stock, we must be having lose data of this then
    if (len(gain_data) == 0):
        gain_data = soup.find_all("span", {"class" : "bse_span_price_change_prcnt txt14R"})
        
    if (len(gain_data) == 0) :
        # There are few stocks for which we don't have the gain data available on moneycontrol
        # TODO: Fetch that data from yahoo finance
        # Display the name of the stock as well
        print("Gain data not available")
        gain = 0
        gain_percent = 0
    else :
        gain_data = gain_data[0].text.split(' ')
        gain = gain_data[0]
        gain_percent = gain_data[1].split('(')[1].split('%')[0]
    return open_price, close_price, gain, gain_percent, volume
    
    
  @staticmethod
  def get_data_from_redirect_url(redirect_content) :
    # metadata includes: Open price, Close price, Gain, Gain%, Volume, prev close,
    # 52W low, 52W high, today low, today high
    
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
    today_open_price, today_close_price, today_gain, today_gain_percent, today_volume = moneycontrol_data_extractor.get_today_open_close_gain_volume(redirect_content)
    today_data = packed_data_today(today_low, today_high, fifty_two_week_low, fifty_two_week_high, today_open_price, today_close_price, today_gain, today_gain_percent, today_volume)
    return prev_close_val, today_data, moving_averages
      
  @staticmethod
  def get_hourly_movers(url, num_stocks, num_days_for_moving_average, delta_from_fifty_week_low) :
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, "lxml")
    table = soup.find_all("div", {"class" : "bsr_table bsr_table930 hist_tbl"})
    ctr = 0
    output = []
    nearly_fifty_two_week_low_stocks = []
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
        span_section = row.find_all("span", {"class" : "gld13 disin"})
        redirect_url = moneycontrol_data_extractor.get_redirect_url(span_section)
        redirect_page = requests.get(redirect_url)
        redirect_content = redirect_page.content
        prev_close_val, today_data, moving_averages = moneycontrol_data_extractor.get_data_from_redirect_url(redirect_content)

        cols = [x.text.strip() for x in cols]
        name = cols[0].split('\n')[0]
        # We have got all the data now, fill it in the schema
        row_data.append(name)
        row_data.append(prev_close_val)
        
        # Hourly open price
        row_data.append(cols[1])
        
        # Hourly close price
        row_data.append(cols[2])
        
        # Hourly gain
        row_data.append(cols[3])
        
        # Hourly gain%
        row_data.append(cols[4])
        
        # Current price
        row_data.append(cols[5])
        row_data.append(today_data.fifty_two_week_low)
        row_data.append(today_data.fifty_two_week_high)
        row_data.append(today_data.low)
        row_data.append(today_data.high)
        row_data.append(moving_averages[0][1])
        row_data.append(moving_averages[1][1])
        row_data.append(moving_averages[2][1])
        row_data.append(moving_averages[3][1])
        row_data.append(moving_averages[4][1])
        row_data.append(today_data.volume)
        
        closing_val = cols[2].replace(',', '')
        if (float(today_data.fifty_two_week_low) * delta_from_fifty_week_low > float(closing_val)) :
          print("Name: ", name, " closing val: ", closing_val, " 52W low: ", today_data.fifty_two_week_low)
          nearly_fifty_two_week_low_stocks.append(name)
            
            
        # Setup an alert when stock breaches it's MA
        signal = '-'
        # cols[5] is current value of the stock which can be of the form 4,234.45
        # we need to convert this to 4234.45 in float for a valid comparison
        val = cols[5].replace(',', '')
        if ((moving_averages[moving_avg_idx][1]) == "-") :
            print("No ", num_days_for_moving_average, " moving data available for: ", name)
        else :
          if (float(val) < float(moving_averages[moving_avg_idx][1])) :
            signal = 'B'
            print("Stock : ", name , " has gone below the : ", num_days_for_moving_average, " days moving average")
          else :
            print("Stock : ", name, " has gone past the moving average")
            signal = 'S'            
        
        row_data.append(signal)
        output.append(row_data)
        ctr += 1
        if (ctr > num_stocks):
          break

    return output, nearly_fifty_two_week_low_stocks

  @staticmethod
  def get_daily_movers(url, num_stocks, num_days_for_moving_average) :
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, "lxml")
    table = soup.find_all("div", {"class" : "bsr_table hist_tbl_hm"})
    ctr = 0
    output = []
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
        span_section = row.find_all("span", {"class" : "gld13 disin"})
        
        # We are only interested in rows which have span section "gld13 disin"
        if (len(span_section) == 0) :
          continue;
        redirect_url = moneycontrol_data_extractor.get_redirect_url(span_section)
        redirect_page = requests.get(redirect_url)
        redirect_content = redirect_page.content
        prev_close_val, today_data, moving_averages = moneycontrol_data_extractor.get_data_from_redirect_url(redirect_content)

        cols = [x.text.strip() for x in cols]
        name = cols[0].split('\n')[0]
      
        # We have got all the data now, fill it in the schema
        row_data.append(name)
        row_data.append(prev_close_val)
        row_data.append(today_data.open_price)
        row_data.append(today_data.close_price)
        row_data.append(today_data.gain)
        row_data.append(today_data.gain_percent)
        row_data.append(today_data.fifty_two_week_low)
        row_data.append(today_data.fifty_two_week_high)
        row_data.append(today_data.low)
        row_data.append(today_data.high)
        row_data.append(moving_averages[0][1])
        row_data.append(moving_averages[1][1])
        row_data.append(moving_averages[2][1])
        row_data.append(moving_averages[3][1])
        row_data.append(moving_averages[4][1])
        row_data.append(today_data.volume)
        
        # Setup an alert when stock breaches it's MA
        signal = 'B'
        if (float(today_data.close_price) < float(moving_averages[moving_avg_idx][1])) :
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
