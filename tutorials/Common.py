#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:05:21 2020

@author: nishant.gupta
"""

# Buy and sell decision params 
class DecisionParams:
    def __init__(self, rsi_level, min_obv_slope, max_obv_slope, adx, \
                 stop_loss_pct = 0, stop_loss_adx_threshold = 0):
        self.rsi_level = rsi_level
        self.min_obv_slope = min_obv_slope
        self.max_obv_slope = max_obv_slope
        self.adx = adx
        self.stop_loss_pct = stop_loss_pct
        self.stop_loss_adx_threshold = stop_loss_adx_threshold