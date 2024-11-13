#!/usr/bin/python
# -*- coding: UTF-8 -*-
import twstock

twstock.__update_codes()
print("-------------------------")
print(twstock.codes['2330']) 
stock = twstock.Stock('2330')
print(stock.date[0])
print(stock.price) # 回傳各日之收盤價
#print(stock.high)  # 回傳各日之最高價
stock.fetch(2012, 10)
print(stock.date[0])
print(stock.price)
print("-------------------------")
print(twstock.codes['8272']) 
print(twstock.codes['8272'].group) 
#stock = twstock.Stock('8272')
#print(stock.date[0])
#print(stock.price)
print("-------------------------")
print(twstock.codes['2646']) 
print(twstock.codes['2646'].group) 
print("-------------------------")
print(twstock.codes['7708']) 
print(twstock.codes['7708'].group) 