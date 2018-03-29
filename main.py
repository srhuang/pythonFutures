#=============================
#name:main.py
#argument:
#author:srhuang
#email:lukyandy3162@gmail.com
#=============================

#===============
#import section
#===============
import sys
import os
from os.path import exists
import datetime, calendar
from dateutil.relativedelta import *

#================
#variable section
#================
year = 2018
month = 03
OHLC_dir="OHLC/"
OHLC_list=[]
OHLC_pre_list=[]

#=================
#argument section
#=================

#=================
#function section
#=================

#===============
#progress start
#===============
#'''
num_days = calendar.monthrange(year, month)[1]
days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
for day in days:
	#skip the Saturday and Sunday
	if day.weekday()==5 or day.weekday()==6:
		continue
	#Stop at today
	if day >= datetime.datetime.today().date():
		break
	#start daily parsing
	os.system("python dailyProcessor.py %s %s %s"%(year, month, day.day))
#'''
#calculate the OHLC files for MA
num_days = calendar.monthrange(year, month)[1]
days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
for day in days:
	#skip the Saturday and Sunday
	if day.weekday()==5 or day.weekday()==6:
		continue
	#Stop at today
	if day >= datetime.datetime.today().date():
		break
	#check the OHLC file
	OHLC_file="OHLC_"+str(year)+str(month).zfill(2)+str(day.day).zfill(2)+".csv"
	if exists(OHLC_dir+OHLC_file):
		OHLC_list+=[OHLC_file]
print OHLC_list

#calculate pre month
d = datetime.date(year, month, 1) - relativedelta(months=1)
premonth = d.month
num_days = calendar.monthrange(year, premonth)[1]
days = [datetime.date(year, premonth, day) for day in range(1, num_days+1)]
for day in days:
	#skip the Saturday and Sunday
	if day.weekday()==5 or day.weekday()==6:
		continue
	#Stop at today
	if day >= datetime.datetime.today().date():
		break
	#check the OHLC file
	OHLC_file="OHLC_"+str(year)+str(premonth).zfill(2)+str(day.day).zfill(2)+".csv"
	if exists(OHLC_dir+OHLC_file):
		OHLC_pre_list+=[OHLC_file]
print OHLC_pre_list

#draw the candle stick
num_days = calendar.monthrange(year, month)[1]
days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
for day in days:
	#skip the Saturday and Sunday
	if day.weekday()==5 or day.weekday()==6:
		continue
	#Stop at today
	if day >= datetime.datetime.today().date():
		break
	#check the OHLC file
	OHLC_file="OHLC_"+str(year)+str(month).zfill(2)+str(day.day).zfill(2)+".csv"
	if not exists(OHLC_dir+OHLC_file):
		continue
	#start draw candle stick
	index=OHLC_list.index(OHLC_file)
	if index==0:
		if not OHLC_pre_list:
			print "OHLC_pre_list is empty."
			continue
		os.system("python candleStick.py " + OHLC_dir+OHLC_file+" "+OHLC_dir+OHLC_pre_list[-1])
	else:
		os.system("python candleStick.py " + OHLC_dir+OHLC_file+" "+OHLC_dir+OHLC_list[index-1])

