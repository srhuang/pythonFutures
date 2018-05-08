# -*- coding: UTF-8 -*-
#=============================
#name:momentum_policy.py
#argument:
# current day OHLC      :csv file	
#author:srhuang
#email:lukyandy3162@gmail.com
#=============================

#===============
#import section
#===============
import os
import sys
from os.path import exists
import datetime

#================
#variable section
#================
output_file="momentum_policy.csv"
take_profit=60
stop_loss=20

entry_signal=20
entry_price=0
entry_time=0
exit_price=0
exit_time=0

direction=0

open_point=0 #開盤
OrderTime=0 #建倉時間
OrderPrice=0 #建倉價格
CoverTime=0 #平倉時間
CoverPrice=0 #平倉價格
profit=0

check_next=2

#=================
#argument section
#=================
current_file_name=sys.argv[1]

#=================
#function section
#=================

#===============
#progress start
#===============
print ">>>>> "+os.path.basename(__file__)+" "+sys.argv[1]

#Parsing OHLC
if exists(current_file_name):
  input_file = open ( current_file_name,"r" )
  num_lines = sum(1 for line in open(current_file_name))
else:
  print current_file_name+" is NOT exist."
  sys.exit(0)

#read OHLC data
lineList = input_file.readlines()
line_count=0
for line in lineList:
	line_count+=1
	Input=line.split(" ")
	if line_count==num_lines:
		break

	open_price=int(Input[1])
	high_price=int(Input[2])
	low_price=int(Input[3])
	close=int(Input[4])

	#keep the open price
	if open_point==0:
		open_point=int(Input[1])

	if line_count==num_lines-1 and OrderPrice!=0 and CoverPrice==0:
		CoverPrice=close
		CoverTime=Input[0]
		break

	#calculate the entry price
	if entry_price==0 and ((int(Input[4])>open_point+entry_signal) or (int(Input[4])<open_point-entry_signal)):
		entry_price=int(Input[4])
		entry_time=Input[0]
		if entry_price>open_point:
			#entry_price=open_point+20
			direction=1
		else:
			#entry_price=open_point-20
			direction=-1
		continue

	#now_time=datetime.datetime.strptime(Input[0], "%H:%M:%S")
	if OrderPrice==0 and entry_price<int(Input[2]) and entry_price>int(Input[3]):
		OrderPrice=entry_price
		OrderTime=Input[0]
		#continue

	#check next candle stick
	
	if OrderPrice!=0 and check_next<2 and exit_price==0:
		
		if direction==1 and open_price>close:
			print "Check Next candlestick is Wrong."
			exit_price=close
			exit_time=Input[0]
		if direction==-1 and close>open_price:
			print "Check Next candlestick is Wrong."
			exit_price=close
			exit_time=Input[0]
		check_next+=1

	#wait for exit price
	if OrderPrice!=0 and CoverPrice==0:
		if direction==1:
			if (high_price-OrderPrice)>=take_profit:
				CoverPrice=OrderPrice+take_profit
				#exit_price=CoverPrice
				CoverTime=Input[0]
			if (OrderPrice-low_price)>=stop_loss:
				CoverPrice=OrderPrice-stop_loss
				CoverTime=Input[0]
		if direction==-1:
			if (OrderPrice-low_price)>=take_profit:
				CoverPrice=OrderPrice-take_profit
				#exit_price=CoverPrice
				CoverTime=Input[0]
			if (low_price-OrderPrice)>=stop_loss:
				CoverPrice=OrderPrice+stop_loss
				CoverTime=Input[0]
		continue
'''
	if OrderPrice!=0 and CoverPrice==0 and exit_price<=int(Input[2]) and exit_price>=int(Input[3]):
		CoverPrice=exit_price
		CoverTime=Input[0]
'''


#calculate profit
if direction==1:
	profit=CoverPrice-OrderPrice
else:
	profit=OrderPrice-CoverPrice

print "Open Price:\t\t", open_point
print "Entry Price:\t", entry_price, entry_time, direction
print "Order Price:\t", OrderPrice, OrderTime
print "Exit Price:\t\t", exit_price, exit_time
print "Cover Price:\t", CoverPrice, CoverTime
print "Profit:\t", profit
with open(output_file, "a") as myfile:
    myfile.write(current_file_name.split("_")[1].split(".")[0]+" "+str(profit)+"\n")

