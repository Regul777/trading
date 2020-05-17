#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 19:24:40 2020

@author: nishant.gupta
"""

class string_util:
    @staticmethod
    def get_processed_data_string(data):
        # converting 23,200 we want to convert it to 23200
        # converting (23,200) we want to -23200
        # we are getting '-' in case of missing data on the page
        # however, ASCII value is not 45 (for '-').
        # Having following temporaily based on :
        # https://stackoverflow.com/questions/631406/what-is-the-difference-between-em-dash-151-and-8212
        print("**********************************")
        print("Data: ", data)
        if (len(data) == 1 and (ord(data) == 8212) or data == '-'):
            return 0
        data = data.replace(',', '')
        data = data.replace('(', '-')
        data = data.replace(')', '')
        return float(data)
    
    @staticmethod
    def get_processed_data(data):
        # sample data: 155 168 (200) 120 (100)
        # we want to convert this to a list : 155 168 -200 120 -100
        processed_data = []
        data = data.split('\n')
        for data_string in data:
            processed_data.append(string_util.get_processed_data_string(data_string))              
        return processed_data