#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:01:01 2020

@author: nishant.gupta
"""

# This strategy is based on RSI, ADX, OBV slopes, Renko chart and Fibonacci retraction
# Typical usage: 
# Specify buy, sell and common params 
# Specify run specific data in Strategy_Runner object
# Call Strategy_Runner.Run()
class Strategy1:
    def __init__(self, buy_params, sell_params, adx_threshold_for_fib_buy,\
                 adx_threshold_for_fib_sell, enable_using_fib_retraction) :
        self.buy_params = buy_params
        self.sell_params = sell_params
        self.adx_threshold_for_fib_buy = adx_threshold_for_fib_buy
        self.adx_threshold_for_fib_sell = adx_threshold_for_fib_sell
        self.enable_using_fib_retraction = enable_using_fib_retraction
    
    def should_buy_now(self, current_state_vals) :
        if (current_state_vals.rsi < self.buy_params.rsi_level and \
            current_state_vals.obv_slope < self.buy_params.max_obv_slope and \
            current_state_vals.obv_slope > self.buy_params.min_obv_slope and \
            current_state_vals.adx > self.buy_params.adx) :
            return True

        # If we are in uptrend and price goes below fibonacci support and also ADX is strong
        if (self.enable_using_fib_retraction == True) :
            if (current_state_vals.adx > self.adx_threshold_for_fib_buy and \
                current_state_vals.current_price != -1 and \
                current_state_vals.fib_support != -1 and \
                current_state_vals.current_price < current_state_vals.fib_support) :
                print("***************Buy based on Fibonacci*****************")
                return True

        return False
    
    def should_sell_now(self, current_state_vals) :
        if (current_state_vals.rsi > self.sell_params.rsi_level and \
            current_state_vals.obv_slope > self.sell_params.min_obv_slope and \
            current_state_vals.obv_slope < self.sell_params.max_obv_slope and \
            current_state_vals.adx > self.sell_params.adx) :
            return True

        # If we are in down trend and price exceeds the fibonacci resistance and also ADX is strong
        if (self.enable_using_fib_retraction == True) :
            if (current_state_vals.adx > self.adx_threshold_for_fib_sell and \
                current_state_vals.current_price != -1 and \
                current_state_vals.fib_resistance != -1 and \
                current_state_vals.current_price > current_state_vals.fib_resistance) :
                print("***************Sell based on Fibonacci*****************")
                return True

        return False
    
    def should_sell_based_on_stop_loss(self, current_state_vals, buy_price) :
        if (current_state_vals.current_price < self.sell_params.stop_loss_pct * buy_price and \
            current_state_vals.adx > self.sell_params.stop_loss_adx_threshold) :
            return True
        
        return False
    
# This strategy is based on MACD, Renko chart and Fibonacci retraction
# Typical usage: 
# Specify buy, sell and common params 
# Specify run specific data in Strategy_Runner object
# Call Strategy_Runner.Run()
class Strategy2:
    def __init__(self, buy_params, sell_params, adx_threshold_for_fib_buy,\
                 adx_threshold_for_fib_sell, enable_using_fib_retraction) :
        self.buy_params = buy_params
        self.sell_params = sell_params
        self.adx_threshold_for_fib_buy = adx_threshold_for_fib_buy
        self.adx_threshold_for_fib_sell = adx_threshold_for_fib_sell
        self.enable_using_fib_retraction = enable_using_fib_retraction
    
    def should_buy_now(self, current_state_vals) :
        if (current_state_vals.bar_num >= self.buy_params.bar_num and \
            current_state_vals.macd > current_state_vals.macd_signal and \
            current_state_vals.macd_slope > current_state_vals.macd_signal_slope):
            return True

        # If we are in uptrend and price goes below fibonacci support and also ADX is strong
        if (self.enable_using_fib_retraction == True) :
            if (current_state_vals.adx > self.adx_threshold_for_fib_buy and \
                current_state_vals.current_price != -1 and \
                current_state_vals.fib_support != -1 and \
                current_state_vals.current_price < current_state_vals.fib_support) :
                print("***************Buy based on Fibonacci*****************")
                return True

        return False
    
    def should_sell_now(self, current_state_vals) :
        if (current_state_vals.bar_num <= self.sell_params.bar_num and \
            current_state_vals.macd < current_state_vals.macd_signal and \
            current_state_vals.macd_slope < current_state_vals.macd_signal_slope) :
            return True

        # If we are in down trend and price exceeds the fibonacci resistance and also ADX is strong
        if (self.enable_using_fib_retraction == True) :
            if (current_state_vals.adx > self.adx_threshold_for_fib_sell and \
                current_state_vals.current_price != -1 and \
                current_state_vals.fib_resistance != -1 and \
                current_state_vals.current_price > current_state_vals.fib_resistance) :
                print("***************Sell based on Fibonacci*****************")
                return True

        return False
    
    def should_sell_based_on_stop_loss(self, current_state_vals, buy_price) :
        if (current_state_vals.current_price < self.sell_params.stop_loss_pct * buy_price and \
            current_state_vals.adx > self.sell_params.stop_loss_adx_threshold) :
            return True
        
        return False
            
            