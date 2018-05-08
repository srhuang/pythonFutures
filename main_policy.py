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
month = 02
make_up_days=[str(datetime.date(2018, 03, 31)), str(datetime.date(2018, 12, 22))]
OHLC_dir="OHLC/"
OHLC_list=[]
OHLC_pre_list=[]
OHLC_current_month=OHLC_dir+"OHLC_"+str(year).zfill(4)+str(month).zfill(2)+".csv"
MAlen = 60
policy_profit="momentum_policy.csv"
#=================
#argument section
#=================

#=================
#function section
#=================

#===============
#progress start
#===============
print "Make-up Days : "
print make_up_days

#remove the profit file
if exists(policy_profit):
	os.remove(policy_profit)

#draw the candle stick
num_days = calendar.monthrange(year, month)[1]
days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
for day in days:
	#check the OHLC file
	OHLC_file="OHLC_"+str(year)+str(month).zfill(2)+str(day.day).zfill(2)+".csv"
	if not exists(OHLC_dir+OHLC_file):
		continue
	os.system("python momentum_policy.py " + OHLC_dir+OHLC_file)

#calculate profit
total_profit=0
if exists(policy_profit):
  input_file = open ( policy_profit,"r" )
else:
  print current_file_name+" is NOT exist."
  sys.exit(0)

lineList = input_file.readlines()
for line in lineList:
	Input=line.split(" ")
	#print int(Input[1])
	total_profit+=int(Input[1])

print "Total Profit : "+ str(total_profit)
