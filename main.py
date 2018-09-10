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
month = 9
make_up_days=[str(datetime.date(2018, 03, 31)), str(datetime.date(2018, 12, 22))]
OHLC_dir="OHLC/"
OHLC_list=[]
OHLC_pre_list=[]
OHLC_current_month=OHLC_dir+"OHLC_"+str(year).zfill(4)+str(month).zfill(2)+".csv"
MAlen = 60
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

num_days = calendar.monthrange(year, month)[1]
days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
for day in days:
	#skip the Sunday
	if day.weekday()==6:
		continue
	#skip Saturday the check the make-up day
	if day.weekday()==5 and (str(day) not in make_up_days):
		continue
	#Stop at today
	if day >= datetime.datetime.today().date():
		break
	#start daily parsing
	os.system("python dailyProcessor.py %s %s %s"%(year, month, day.day))

#calculate the OHLC files
num_days = calendar.monthrange(year, month)[1]
days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
for day in days:
	#check the OHLC file
	OHLC_file="OHLC_"+str(year)+str(month).zfill(2)+str(day.day).zfill(2)+".csv"
	if exists(OHLC_dir+OHLC_file):
		OHLC_list+=[OHLC_file]
print OHLC_list

#calculate pre month
d = datetime.date(year, month, 1) - relativedelta(months=1)
premonth = d.month
OHLC_pre_month=OHLC_dir+"OHLC_"+str(year).zfill(4)+str(premonth).zfill(2)+".csv"

#combine all OHLC in one month
total_amount=0
with open(OHLC_current_month, 'w') as outfile:
	#write the pre month
	if not exists(OHLC_pre_month):
		print str(day.year).zfill(4)+str(day.month).zfill(2)+str(day.day).zfill(2)+" OHLC_pre_month is empty."
	else:
		with open(OHLC_pre_month) as pre_infile:
			num_lines = sum(1 for line in open(OHLC_pre_month))
			line_count=1
			for line in pre_infile:
				if line_count > (num_lines-MAlen):
					outfile.write(line)
				line_count+=1

	#write the current month
	for fname in OHLC_list:
		with open(OHLC_dir+fname) as infile:
			num_lines = sum(1 for line in open(OHLC_dir+fname))
			line_count=1
			for line in infile:
				if line_count != num_lines:
					outfile.write(fname.split("_")[1].split(".")[0]+" "+line)
					total_amount+=1
				line_count+=1
print "#days:"+str(len(OHLC_list))+" , total amount : "+str(total_amount)

#draw the candle stick
num_days = calendar.monthrange(year, month)[1]
days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
for day in days:
	#check the OHLC file
	OHLC_file="OHLC_"+str(year)+str(month).zfill(2)+str(day.day).zfill(2)+".csv"
	if not exists(OHLC_dir+OHLC_file):
		continue
	#start draw candle stick
	index=OHLC_list.index(OHLC_file)
	os.system("python candleStick.py " + OHLC_dir+OHLC_file+" "+OHLC_current_month)
