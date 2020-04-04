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
    
    def should_buy_now(self, rsi, slope, adx, fibonacci_support = -1, price = -1) :
        if (rsi < self.buy_params.rsi_level and slope < self.buy_params.max_obv_slope and \
            slope > self.buy_params.min_obv_slope and adx > self.buy_params.adx) :
            return True

        # If we are in uptrend and price goes below fibonacci support and also ADX is strong
        if (self.enable_using_fib_retraction == True) :
            if (adx > self.adx_threshold_for_fib_buy and price != -1 and \
                fibonacci_support != -1 and price < fibonacci_support) :
                print("***************Buy based on Fibonacci*****************")
                return True

        return False
    
    def should_sell_now(self, rsi, slope, adx, fibonacci_resistance = -1, price = -1) :
        if (rsi > self.sell_params.rsi_level and slope > self.sell_params.min_obv_slope and \
            slope < self.sell_params.max_obv_slope and adx > self.sell_params.adx) :
            return True

        # If we are in down trend and price exceeds the fibonacci resistance and also ADX is strong
        if (self.enable_using_fib_retraction == True) :
            if (adx > self.adx_threshold_for_fib_sell and price != -1 and \
                fibonacci_resistance != -1 and price > fibonacci_resistance) :
                print("***************Sell based on Fibonacci*****************")
                return True

        return False
    
    def should_sell_based_on_stop_loss(self, current_price, buy_price, adx) :
        if (current_price < self.sell_params.stop_loss_pct * buy_price and \
            adx > self.sell_params.stop_loss_adx_threshold) :
            return True
        
        return False
            