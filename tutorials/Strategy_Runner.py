#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:35:13 2020

@author: nishant.gupta
"""

import numpy as np
import pandas as pd

from kpis import KPI

# Bundle Run results into the object
class Strategy_Runner_Result:
    def __init__(self, num_profits, num_losses, cummulative_cagr, \
                 cummulative_sharpe_ratio, cummulative_dd, modified_interday_data,\
                 individual_cagr, individual_sharpe_ratio, individual_dd) :
        self.num_profits = num_profits
        self.num_losses = num_losses
        self.cummulative_cagr = cummulative_cagr
        self.cummulative_sharpe_ratio = cummulative_sharpe_ratio
        self.cummulative_dd = cummulative_dd
        self.modified_interday_data = modified_interday_data
        self.individual_cagr = individual_cagr
        self.individual_sharpe_ratio = individual_sharpe_ratio
        self.individual_dd = individual_dd
        
# TODO: Make Strategy Runner a generic class which can take any kind of data
# Presently it's tightly coupled to data havong "RSI", "ADX", "R*", "S*" etc. params
class Strategy_Runner:
    def __init__(self, strategy, tickers, interday_data) :
        self.strategy = strategy
        self.tickers = tickers
        self.interday_data = interday_data
        
    def Run(self) :
        profit = 0
        loss = 0
        for ticker in self.tickers:
            print("calculating daily returns for ", ticker)
            buy = 0
            buy_price = 0
            for i in range(len(self.interday_data.ohlc_renko[ticker])):
                if (i < 14):
                    self.interday_data.tickers_ret[ticker].append(0)   
                    self.interday_data.tickers_state[ticker].append('NA')
                    self.interday_data.tickers_signal[ticker].append('NA')
                    continue;
      
                rsi = self.interday_data.ohlc_renko[ticker]["RSI"][i]
                slope = self.interday_data.ohlc_renko[ticker]["obv_slope"][i]
                adx = self.interday_data.ohlc_renko[ticker]["ADX"][i]
                fib_support = self.interday_data.collated_data[ticker]['S1'][i]
                fib_resistance = self.interday_data.collated_data[ticker]['R1'][i]
                current_price = self.interday_data.ohlc_renko[ticker]["Adj Close"][i]
                
                # We first maintain a state of signal into "Signal" column before actually
                # changing the "State" which depends on our previous state ("B" or "S")
                can_buy_now = (self.strategy.should_buy_now(rsi, slope, adx, fib_support, current_price) == True)
                can_sell_now = (self.strategy.should_sell_now(rsi, slope, adx, fib_resistance, current_price) == True)

                if (can_buy_now == True):
                    self.interday_data.tickers_signal[ticker].append('B')
                elif (can_sell_now == True) :
                    self.interday_data.tickers_signal[ticker].append('S')
                else :
                    self.interday_data.tickers_signal[ticker].append('NA')
    
                # If fibonacci levels are not to be used, setting support and resistance as -1
                if (self.strategy.enable_using_fib_retraction == False) :
                    fib_support = -1
                    fib_resistance = -1

                if (buy == 0) :
                    self.interday_data.tickers_ret[ticker].append(0)           
                    if (can_buy_now == True) :
                        print("Buying the: ", ticker, " at ", current_price)
                        print("Bar num: ", self.interday_data.ohlc_renko[ticker]["bar_num"][i], \
                              "Slope: ", self.interday_data.ohlc_renko[ticker]["obv_slope"][i], \
                              " RSI: ", self.interday_data.ohlc_renko[ticker]["RSI"][i])
                        buy = 1
                        buy_price = current_price
                        self.interday_data.tickers_state[ticker].append('B')
                    else:
                        self.interday_data.tickers_state[ticker].append('NA')
                else :
                    if (can_sell_now == True) :
                        buy = 0
                        self.interday_data.tickers_ret[ticker].append((current_price / buy_price) - 1)
                        print("Return booked : ", current_price / buy_price)
                        if (buy_price >= current_price) :
                            loss += 1
                        else:
                            profit += 1
                        buy_price = 0
                        self.interday_data.tickers_state[ticker].append('S')
                    elif (self.strategy.should_sell_based_on_stop_loss(current_price, buy_price, adx)) :
                        # We set the stop loss at strategy.sell_params.stop_loss_pct % of the buy price.
                        # Also, making sure if there is a strong falling trend or not
                        self.interday_data.tickers_ret[ticker].append((current_price / buy_price) - 1)
                        self.interday_data.tickers_state[ticker].append('S')
                        print("Return booked : ", current_price / buy_price)
                        buy_price = 0
                        buy = 0
                        loss += 1
                    else :
                        self.interday_data.tickers_ret[ticker].append(0)
                        self.interday_data.tickers_state[ticker].append('Hold')
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
                                      cagr, sharpe_ratios, max_drawdown)