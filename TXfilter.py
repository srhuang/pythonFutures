#=============================
#name:TXfilter.py
#argument:
#	input file:csv file
#author:srhuang
#email:lukyandy3162@gmail.com
#=============================

#===============
#import section
#===============
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import sys
import os
from os.path import exists
import calendar

#================
#variable section
#================
outputFolder="TXfilter/"
PRODUCT="TX"
count=1
intraday_amount=0
afterHours_amount=0
intraday_cross_month=0
afterHours_cross_month=0

#=================
#argument section
#=================
file_path=sys.argv[1]
file_name=sys.argv[1].split('/')[1].split('_')
year=file_name[1].zfill(4)
month=file_name[2].zfill(2)
day=file_name[3].split('.')[0].zfill(2)

#=================
#function section
#=================
def find_third_wednesdays(year, month):
    wednesdays = [week[calendar.WEDNESDAY] for week in calendar.monthcalendar(year, month)]
    if wednesdays[0] == 0:
    	third_wednesday = wednesdays[3]
    else:
    	third_wednesday = wednesdays[2]
    return third_wednesday

#===============
#progress start
#===============
print ">>>>> "+os.path.basename(__file__)+" "+sys.argv[1]
#print "Current Folder:"+os.getcwd()

#check the input file
if exists(file_path):
	input_file = open ( file_path,"r" )
else:
	print file_path+" is NOT exist."
	sys.exit(0)

#check and open the output file
if exists(outputFolder+PRODUCT+"_"+year+month+day+".csv"):
	print PRODUCT+"_"+year+month+day+".csv" + " is already exist."
	sys.exit(0)
else:
	output_file = open(outputFolder+PRODUCT+"_"+year+month+day+".csv",'w')

#calculate the ticketday
ticketday=find_third_wednesdays(int(year), int(month))
print "ticketday : "+year+month+str(ticketday).zfill(2)

#determine the contract month
if int(day) > ticketday:
	next_month = int(month)+1
	contract_month = year+str(next_month).zfill(2)
else:
	contract_month = year+month
print "Contract Month : "+contract_month

#write the TX into filter file
lineList = input_file.readlines()
for line in lineList[1:-1]:
	Input=line.replace(" ", "").split(",")
	#non cross month
	if Input[1]==PRODUCT and Input[2]==contract_month:
		if (int(Input[3])>=84500) and (int(Input[3])<=134500):
			intraday_amount+=int(Input[5])
			output_file.write(line)
		else:
			afterHours_amount+=int(Input[5])
	#cross month
	if Input[1]==PRODUCT and (contract_month+"/") in Input[2]:
		if (int(Input[3])>=84500) and (int(Input[3])<=134500):
			intraday_cross_month+=int(Input[5])
		else:
			afterHours_cross_month+=int(Input[5])

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

#total amount
print "total amount:", intraday_total+afterHours_total
print "<<<<< "+os.path.basename(__file__)+" done."