#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:05:21 2020

@author: nishant.gupta
"""

# Buy and sell decision params 
class DecisionParams:
    def __init__(self, rsi_level = -1, min_obv_slope = -1, max_obv_slope = -1, adx = -1, \
                 stop_loss_pct = 0, stop_loss_adx_threshold = 0, bar_num = 0):
        self.rsi_level = rsi_level
        self.min_obv_slope = min_obv_slope
        self.max_obv_slope = max_obv_slope
        self.adx = adx
        self.stop_loss_pct = stop_loss_pct
        self.stop_loss_adx_threshold = stop_loss_adx_threshold
        self.bar_num = bar_num
        
class Current_state_values:
    def __init__(self, rsi, bar_num, obv_slope, adx,\
                 fib_support, fib_resistance, current_price,\
                 macd, macd_signal, macd_slope, macd_signal_slope):
        self.rsi = rsi
        self.bar_num = bar_num
        self.obv_slope = obv_slope
        self.adx = adx
        self.fib_support = fib_support
        self.fib_resistance = fib_resistance
        self.current_price = current_price
        self.macd = macd
        self.macd_signal = macd_signal
        self.macd_slope = macd_slope
        self.macd_signal_slope = macd_signal_slope