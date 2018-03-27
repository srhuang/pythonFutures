# -*- coding: UTF-8 -*-

#載入相關套件及函數
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import sys
import os
from os.path import exists
import calendar

#check and create output folder
print os.path.basename(__file__)
print "Current Folder:"+os.getcwd()
outputFolder=sys.argv[2]

file_path=sys.argv[1]
test=sys.argv[1].split('/')[1].split('_')
day=test[3].split('.')[0]

def find_third_wednesdays(year, month):
    wednesdays = [week[calendar.WEDNESDAY] for week in calendar.monthcalendar(year, month)]
    if wednesdays[0] == 0:
    	third_wednesday = wednesdays[3]
    else:
    	third_wednesday = wednesdays[2]
    return third_wednesday

ticketday=find_third_wednesdays(int(test[1]), int(test[2]))
print "ticketday : "+test[1]+test[2]+str(ticketday).zfill(2)

#print day
if int(day) >ticketday:
	next_month=int(test[2])+1
	month_string=test[1]+str(next_month).zfill(2)
else:
	month_string= test[1]+test[2]
print "month_string : "+month_string
PRODUCT="TX"

#Prepare the output file
file = open(outputFolder+PRODUCT+"_"+test[1]+test[2]+test[3],'w')

#Filter the TX 台指期大台, MTX 小台
count=1
intraday_amount=0
afterHours_amount=0
intraday_cross_month=0
afterHours_cross_month=0
fileHandle = open ( file_path,"r" )
lineList = fileHandle.readlines()
for line in lineList[1:-1]:
	Input=line.replace(" ", "").split(",")
	#non cross month
	if Input[1]==PRODUCT and Input[2]==month_string:
		if (int(Input[3])>=84500) and (int(Input[3])<=134500):
			intraday_amount+=int(Input[5])
			file.write(line)
		else:
			afterHours_amount+=int(Input[5])
	#cross month
	if Input[1]==PRODUCT and (month_string+"/") in Input[2]:
		if (int(Input[3])>=84500) and (int(Input[3])<=134500):
			intraday_cross_month+=int(Input[5])
		else:
			afterHours_cross_month+=int(Input[5])
	count+=1
# Intrday
print "intraday amount:",intraday_amount/2
print "intraday cross month:",intraday_cross_month/4
intraday_total=intraday_amount/2+intraday_cross_month/4
print "Intraday trading:",intraday_total

#After afterHours
print "After-hours amount:",afterHours_amount/2
print "After-hours cross month:",afterHours_cross_month/4
afterHours_total=afterHours_amount/2+afterHours_cross_month/4
print "After-hours trading:", afterHours_total

print "total amount:", intraday_total+afterHours_total
