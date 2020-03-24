#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 15:57:03 2020

@author: nishant.gupta
"""

# cron for this: 0,5,10,15,20,20,35,40,45,50,55 9,10,11,12,13,14,15,16,17 * * *
import pandas as pd
from mail_utils import smtp_client
from moneycontrol_movers_bse import moneycontrol_data_extractor

moving_average_to_consider = 10

hourly_num_stocks = 20
delta_from_fifty_two_week_low = 1.02
hourly_schema = ['Name', 'Prev Close', 'Open Price', 'Close Price', 'Gain', 'Gain %', 'Current Price', '52Week low', '52Week high', 'Today low', 'Today high', '5 MA', '10 MA', '20 MA', '50 MA', '200 MA', 'Volume', 'Signal']
hourly_gain_url = 'https://www.moneycontrol.com/stocks/marketstats/hourly_gain/bse/curr_hour/index.php'
hourly_loss_url = 'https://www.moneycontrol.com/stocks/marketstats/hourly_loss/bse/curr_hour/index.php'
hourly_gainers, temp  = moneycontrol_data_extractor.get_hourly_movers(hourly_gain_url, hourly_num_stocks, moving_average_to_consider, delta_from_fifty_two_week_low)
hourly_gainers = pd.DataFrame(hourly_gainers, columns = hourly_schema)
hourly_losers, nearly_fifty_two_week_low_stocks = moneycontrol_data_extractor.get_hourly_movers(hourly_loss_url, hourly_num_stocks, moving_average_to_consider, delta_from_fifty_two_week_low)
hourly_losers = pd.DataFrame(hourly_losers, columns = hourly_schema)

# Alert for potential 52W low
smtp_client.send_mail("niku2907@gmail.com", str(nearly_fifty_two_week_low_stocks), "Maybe 52W low")

mail_schema = ['Name', 'Gain %']

# Alert for potential buy positions based on MA
interesting_stocks = hourly_losers[hourly_losers['Signal'] == 'B']
message = interesting_stocks[mail_schema].values.tolist()
smtp_client.send_mail("niku2907@gmail.com", str(message), "Buys based on hourly losers")

# Alert for potential sell positions based on MA
interesting_stocks = hourly_losers[hourly_gainers['Signal'] == 'S']
message = interesting_stocks[mail_schema].values.tolist()
smtp_client.send_mail("niku2907@gmail.com", str(message), "Sells based on hourly gainers")

print(message)
print(hourly_gainers)
print(hourly_losers)

print(nearly_fifty_two_week_low_stocks)