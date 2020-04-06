#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:35:13 2020

@author: nishant.gupta
"""

import heapq
import math
import numpy as np
import pandas as pd

from kpis import KPI
from Common import Current_state_values

# Bundle Run results into the object
class Strategy_Runner_Result:
    def __init__(self, num_profits, num_losses, cummulative_cagr, \
                 cummulative_sharpe_ratio, cummulative_dd, modified_interday_data,\
                 individual_cagr, individual_sharpe_ratio, individual_dd, resultant_money) :
        self.num_profits = num_profits
        self.num_losses = num_losses
        self.cummulative_cagr = cummulative_cagr
        self.cummulative_sharpe_ratio = cummulative_sharpe_ratio
        self.cummulative_dd = cummulative_dd
        self.modified_interday_data = modified_interday_data
        self.individual_cagr = individual_cagr
        self.individual_sharpe_ratio = individual_sharpe_ratio
        self.individual_dd = individual_dd
        self.resultant_money = resultant_money
        
# TODO: Make Strategy Runner a generic class which can take any kind of data
# Presently it's tightly coupled to data havong "RSI", "ADX", "R*", "S*" etc. params
class Strategy_Runner:
    def __init__(self, strategy, tickers, interday_data, num_simultaneous_buy = 1) :
        self.strategy = strategy
        self.tickers = tickers
        self.interday_data = interday_data
        self.buy_list = []
        self.num_simultaneous_buy = num_simultaneous_buy
        
    def Run(self) :
        #TODO: Create a logging framework
        profit = 0
        loss = 0
        resultant_money = {}
        for ticker in self.tickers:
            resultant_money_for_this_ticker = 1
            print("calculating daily returns for ", ticker)
            self.buy_list.clear()
            for i in range(len(self.interday_data.ohlc_renko[ticker])):
                if (i < 14):
                    self.interday_data.tickers_ret[ticker].append(0)   
                    self.interday_data.tickers_state[ticker].append('NA')
                    self.interday_data.tickers_signal[ticker].append('NA')
                    continue;
      
                bar_num = self.interday_data.ohlc_renko[ticker]['bar_num'][i]
                rsi = self.interday_data.ohlc_renko[ticker]["RSI"][i]
                slope = self.interday_data.ohlc_renko[ticker]["obv_slope"][i]
                adx = self.interday_data.ohlc_renko[ticker]["ADX"][i]
                fib_support = self.interday_data.collated_data[ticker]['S1'][i]
                fib_resistance = self.interday_data.collated_data[ticker]['R1'][i]
                current_price = self.interday_data.ohlc_renko[ticker]["Adj Close"][i]
                macd = self.interday_data.ohlc_renko[ticker]['macd'][i]
                macd_signal = self.interday_data.ohlc_renko[ticker]['macd_sig'][i]
                macd_slope = self.interday_data.ohlc_renko[ticker]['macd_slope'][i]
                macd_sig_slope = self.interday_data.ohlc_renko[ticker]['macd_sig_slope'][i]
                current_state_values = Current_state_values(rsi = rsi, bar_num = bar_num, \
                                                            obv_slope = slope, adx = adx, fib_support = fib_support,\
                                                            fib_resistance = fib_resistance, current_price = current_price,
                                                            macd = macd, macd_signal = macd_signal,\
                                                            macd_slope = macd_slope, macd_signal_slope = macd_sig_slope)
                
                # We first maintain a state of signal into "Signal" column before actually
                # changing the "State" which depends on our previous state ("B" or "S")
                can_buy_now = (self.strategy.should_buy_now(current_state_values) == True)
                can_sell_now = (self.strategy.should_sell_now(current_state_values) == True)

                if (can_buy_now == True and can_sell_now == True) :
                    can_buy_now = False
                    can_sell_now = False
                    self.interday_data.tickers_signal[ticker].append('Confused')
                elif (can_buy_now == True):
                    self.interday_data.tickers_signal[ticker].append('B')
                elif (can_sell_now == True) :
                    self.interday_data.tickers_signal[ticker].append('S')
                else :
                    self.interday_data.tickers_signal[ticker].append('NA')
                
                if (can_buy_now == True and can_sell_now == True) :
                    # If both the signals are ON we are in confused state and we don't do any trade
                    can_buy_now = False
                    can_sell_now = False
    
                # If fibonacci levels are not to be used, setting support and resistance as -1
                if (self.strategy.enable_using_fib_retraction == False) :
                    fib_support = -1
                    fib_resistance = -1

                # If we have room to buy then we do based on the buy signal  
                state = ""
                ret = 0
                if (len(self.buy_list) < self.num_simultaneous_buy) :
                    if (can_buy_now == True) :
                        #print("Buying the: ", ticker, " at ", current_price)
                        # Buying at current_price
                        heapq.heappush(self.buy_list, current_price)
                        state += 'B'

                # If we have bought atleast once
                if (len(self.buy_list) > 0) :
                    if (can_sell_now == True) :
                        # If we have to sell then pop the top element of the heap
                        # If we just to make the stop loss decision simply get the top element
                        buy_price = heapq.heappop(self.buy_list)
                        ret = (current_price / buy_price) - 1
                        #print("Return booked : ", current_price / buy_price)
                        if (buy_price >= current_price) :
                            loss += 1
                        else:
                            profit += 1
                        state += " S(" + str(math.floor(buy_price)) + "->" + str(math.floor(current_price)) + ")"
                    elif (self.strategy.should_sell_based_on_stop_loss(current_state_values, self.buy_list[0])) :
                        # We set the stop loss at strategy.sell_params.stop_loss_pct % of the buy price.
                        # Also, making sure if there is a strong falling trend or not
                        buy_price = heapq.heappop(self.buy_list)
                        ret = (current_price / buy_price) - 1
                        state += " S(" + str(math.floor(buy_price)) + "->" + str(math.floor(current_price)) + ")"
                        #print("Return booked : ", current_price / buy_price)
                        loss += 1
                    else :
                        if (state.find('B') != -1) :
                            state += " Hold"
                        else:
                            state = "Hold"
                    
                    assert(len(self.buy_list) <= self.num_simultaneous_buy)
                if (state == "") :
                    state = "NA"
                
                resultant_money_for_this_ticker *= (1 + ret)
                self.interday_data.tickers_ret[ticker].append(ret)
                self.interday_data.tickers_state[ticker].append(state) 
            resultant_money[ticker] = resultant_money_for_this_ticker
            self.interday_data.ohlc_renko[ticker]["ret"] = np.array(self.interday_data.tickers_ret[ticker])
            self.interday_data.ohlc_renko[ticker]["State"] = np.array(self.interday_data.tickers_state[ticker])
            self.interday_data.ohlc_renko[ticker]["Signal"] = np.array(self.interday_data.tickers_signal[ticker])
            self.interday_data.ohlc_renko[ticker].set_index("Date", inplace = True)
        # calculating overall strategy's KPIs
        strategy_df = pd.DataFrame()
        for ticker in self.tickers:
            strategy_df[ticker] = self.interday_data.ohlc_renko[ticker]["ret"]
            strategy_df["ret"] = strategy_df.mean(axis = 1)
        new_cagr = KPI.CAGR(strategy_df)
        new_sharpe = KPI.sharpe(strategy_df,0.025)
        new_dd = KPI.max_dd(strategy_df)

        #calculating individual stock's KPIs
        cagr = {}
        sharpe_ratios = {}
        max_drawdown = {}
        for ticker in self.tickers:
            print("calculating KPIs for ",ticker)      
            cagr[ticker] =  KPI.CAGR(self.interday_data.ohlc_renko[ticker])
            sharpe_ratios[ticker] =  KPI.sharpe(self.interday_data.ohlc_renko[ticker],0.025)
            max_drawdown[ticker] =  KPI.max_dd(self.interday_data.ohlc_renko[ticker])
        
        return Strategy_Runner_Result(profit, loss, new_cagr, new_sharpe, new_dd, self.interday_data,
                                      cagr, sharpe_ratios, max_drawdown, resultant_money)