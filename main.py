import sys
import os
from os.path import exists
import datetime, calendar
year = 2018
month = 03
#today=18
num_days = calendar.monthrange(year, month)[1]
days = [datetime.date(year, month, day) for day in range(1, num_days+1)]

OHLC_dir="OHLC/"
OHLCfiles=[]

#os.system("python dailyProcessor.py %s %s %s"%(year, month, 26))

for day in days:
	if day.weekday()!=5 and day.weekday()!=6:
		#print day.day
		if day >= datetime.datetime.today().date():
			print day,"Escape Future days."
		else:
			os.system("python dailyProcessor.py %s %s %s"%(year, month, day.day))
			#print "check "+tx_dir+"TX_"+str(year)+str(month)+str(day.day)+".csv"
			if exists(OHLC_dir+"OHLC_"+str(year)+str(month).zfill(2)+str(day.day).zfill(2)+".csv"):
				#print "Adding file list : "+str(year)+str(month).zfill(2)+str(day.day).zfill(2)
				OHLCfiles+=[["OHLC_"+str(year)+str(month).zfill(2)+str(day.day).zfill(2)+".csv"]]

#os.system("python %s/candleStick.py %sTX_"%(root_path, tx_dir)+test[1]+test[2]+test[3]+".csv"+" "+candleStick_dir)
print OHLCfiles