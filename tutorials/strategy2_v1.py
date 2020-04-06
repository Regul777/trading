#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 00:34:29 2020

@author: nishant.gupta
"""

# TODO: Tune the numbers for this strategy
# See if we can club strategy1 and strategy2 to get some what good returns for the
# bearish stocks
from Common import DecisionParams
from interday_testing_helper import interday_testing_helper
from Strategy import Strategy2
from Strategy_Runner import Strategy_Runner

tickers = ["INDUSINDBK.BO", "YESBANK.BO"]

interday_data = interday_testing_helper.get_interday_collated_data(tickers, n = 735, delta = 45)
buy_params = DecisionParams(bar_num = 10)

sell_params = DecisionParams(bar_num = -2)

strategy = Strategy2(buy_params = buy_params, sell_params = sell_params, \
                     adx_threshold_for_fib_buy = 50, adx_threshold_for_fib_sell = 50, \
                     enable_using_fib_retraction = True)

strategy_runner = Strategy_Runner(strategy, tickers, interday_data, num_simultaneous_buy = 1)
result = strategy_runner.Run()

# Adding following variables as Spyder is not able to unpack user defined datatype and hence
# values are not visible in the Variable explorer
cummulative_ohlc_data = result.modified_interday_data.ohlc_renko
cummulative_interesting_data = result.modified_interday_data.collated_data
cummulative_cagr = result.cummulative_cagr
cummulative_sharpe_ratio = result.cummulative_sharpe_ratio
cummulative_dd = result.cummulative_dd

individual_cagr = result.individual_cagr
individual_sharpe_ratio = result.individual_sharpe_ratio
individual_dd = result.individual_dd

num_profit = result.num_profits
num_loss = result.num_losses
resultant_money = result.resultant_money