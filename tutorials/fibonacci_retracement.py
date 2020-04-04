#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 17:45:06 2020

@author: nishant.gupta
"""

class resistance_support:
    def __init__(self, resistance, support):
        self.resistance = resistance
        self.support = support
        
class fib_levels:
    def __init__(self, RS1, RS2, RS3):
        self.RS1 = RS1
        self.RS2 = RS2
        self.RS3 = RS3
        
class fib_levels_helper:
    # Xn / Xn+1 = .618
    # Xn / Xn+2 = .382
    # Xn / Xn+3 = .236
    @staticmethod
    def get(prev_high, prev_low, uptrend = True) :
        prev_diff = prev_high - prev_low
        level1 = .236 * prev_diff
        level2 = .382 * prev_diff
        level3 = .618 * prev_diff
        level_to_consider = prev_low
        if (uptrend == True):
            level_to_consider = prev_high
        R1 = level_to_consider + level1
        R2 = level_to_consider + level2
        R3 = level_to_consider + level3
        S1 = level_to_consider - level1
        S2 = level_to_consider - level2
        S3 = level_to_consider - level3
        RS1 = resistance_support(R1, S1)
        RS2 = resistance_support(R2, S2)
        RS3 = resistance_support(R3, S3)  
        return fib_levels(RS1, RS2, RS3)