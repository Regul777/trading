#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 18:43:05 2020

@author: nishant.gupta
"""

# cron for this: 0 16,17 * * *
import pandas as pd
from mail_utils import smtp_client
from moneycontrol_movers_bse import moneycontrol_data_extractor

moving_average_to_consider = 200
daily_num_stocks = 30
daily_schema = ['Name', 'Prev Close', 'Open Price', 'Close Price', 'Gain', 'Gain %', '52Week low', '52Week high', 'Today low', 'Today high', '5 MA', '10 MA', '20 MA', '50 MA', '200 MA', 'Volume', 'Signal', 'MACD Signal']
top_gainers_url = "https://www.moneycontrol.com/stocks/marketstats/bsegainer/index.php"
top_losers_url = "https://www.moneycontrol.com/stocks/marketstats/bseloser/index.php"
top_gainers = moneycontrol_data_extractor.get_daily_movers(top_gainers_url, daily_num_stocks, moving_average_to_consider)
top_gainers = pd.DataFrame(top_gainers, columns = daily_schema)
top_losers = moneycontrol_data_extractor.get_daily_movers(top_losers_url, daily_num_stocks, moving_average_to_consider)
top_losers = pd.DataFrame(top_losers, columns = daily_schema)
print(top_gainers)
print(top_losers)

mail_schema = ['Name', 'Gain %']
interesting_stocks = top_losers[top_losers['Signal'] == 'B']
message = interesting_stocks[mail_schema].values.tolist()
smtp_client.send_mail("niku2907@gmail.com", str(message), "Buys based on today's losers")
print(message)

interesting_stocks = top_gainers[top_gainers['Signal'] == 'B']
message = interesting_stocks[mail_schema].values.tolist()
smtp_client.send_mail("niku2907@gmail.com", str(message), "Buys based on today's gainers")
print(message)


interesting_stocks = top_losers[top_losers['Signal'] == 'S']
message = interesting_stocks[mail_schema].values.tolist()
smtp_client.send_mail("niku2907@gmail.com", str(message), "Sells based on today's losers")
print(message)

interesting_stocks = top_gainers[top_gainers['Signal'] == 'S']
message = interesting_stocks[mail_schema].values.tolist()
smtp_client.send_mail("niku2907@gmail.com", str(message), "Sells based on today's gainers")
print(message)

mail_schema = ['Name', 'Gain %']
interesting_stocks = top_losers[top_losers['MACD Signal'] == 'B']
message = interesting_stocks[mail_schema].values.tolist()
smtp_client.send_mail("niku2907@gmail.com", str(message), "Buys (MACD) based on today's losers")
print(message)

interesting_stocks = top_gainers[top_gainers['MACD Signal'] == 'B']
message = interesting_stocks[mail_schema].values.tolist()
smtp_client.send_mail("niku2907@gmail.com", str(message), "Buys (MACD )based on today's gainers")
print(message)


interesting_stocks = top_losers[top_losers['MACD Signal'] == 'S']
message = interesting_stocks[mail_schema].values.tolist()
smtp_client.send_mail("niku2907@gmail.com", str(message), "Sells (MACD) based on today's losers")
print(message)

interesting_stocks = top_gainers[top_gainers['MACD Signal'] == 'S']
message = interesting_stocks[mail_schema].values.tolist()
smtp_client.send_mail("niku2907@gmail.com", str(message), "Sells (MACD) based on today's gainers")
print(message)