# -*- coding: UTF-8 -*-
#=============================
#name:candleStick.py
#argument:
# current day OHLC      :csv file
# current month OHLC    :csv file
#author:srhuang
#email:lukyandy3162@gmail.com
#=============================

#===============
#import section
#===============
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance
from mpl_finance import candlestick_ohlc
from matplotlib import ticker as mticker
from matplotlib.ticker import NullFormatter
from matplotlib.dates import AutoDateLocator
import matplotlib
import os
import sys
from os.path import exists

#================
#variable section
#================
outputFolder="candleStick/"

OHLC=[]
openprice=0
highPrice=0
lowPrice=0
closeprice=0
line_count=1

MAlen = 60
MA = []
MAValue = 0
maxMA=0
minMA=99999

#=================
#argument section
#=================
current_file_name=sys.argv[1]
month_OHLC_file=sys.argv[2]
current_date=sys.argv[1].split("_")[1].split(".")[0]

#=================
#function section
#=================
def TimetoNumber(time):
  time=time.zfill(6)
  sec=int(time[:2])*3600+int(time[2:4])*60+int(time[4:6])
  return sec

def NumbertoTime(sec):
 TS=str(sec%60).zfill(2)
 sec=sec/60
 TM=str(sec%60).zfill(2)
 sec=sec/60
 TH=str(sec%60).zfill(2)
 return TH+TM+TS

def calculateMAValue(current_date, current_time):
  #get current day line in file
  current_day_line=0
  month_OHLC = open ( month_OHLC_file,"r" )
  for i, line in enumerate(month_OHLC):
    if (line.split(" ")[0] == str(current_date)) and (line.split(" ")[1] == str(current_time)):
      current_day_line=i

  if current_day_line<MAlen:
    return 0
  #parsing the MA data
  MAarray = []
  month_OHLC = open ( month_OHLC_file,"r" )
  for i, line in enumerate(month_OHLC):
    if (i > current_day_line-MAlen) and (i <= current_day_line):
      MAarray+=[int(line.split(" ")[5])]

  MAValue=float(sum(MAarray))/len(MAarray)
  return round(MAValue)

#===============
#progress start
#===============
print ">>>>> "+os.path.basename(__file__)+" "+sys.argv[1]+" "+sys.argv[2]

STime = TimetoNumber('084500')
ETime = TimetoNumber('134500')

#Parsing OHLC
if exists(current_file_name):
  input_file = open ( current_file_name,"r" )
  num_lines = sum(1 for line in open(current_file_name))
else:
  print current_file_name+" is NOT exist."
  sys.exit(0)

#prepare the OHLC
lineList = input_file.readlines()
for line in lineList:
  #print "line count : %s"%(line_count)
  Input=line.split(" ")
  if line_count==1:
    openprice=int(Input[1])
  if line_count==(num_lines-1):
    closeprice=int(Input[4])
  if line_count==num_lines:
    lowPrice=int(Input[0])
    highPrice=int(Input[1])
  else:
    current_time=mdates.date2num(datetime.datetime.strptime(Input[0], "%H:%M:%S"))
    OHLC+=[[current_time, int(Input[1]), int(Input[2]), int(Input[3]), int(Input[4]), int(Input[5])]]
    #print mdates.num2date(current_time).time()
    MAValue=calculateMAValue(current_date, mdates.num2date(current_time).time())
    if MAValue!=0:
      MA.extend([MAValue])
  line_count+=1

#Check month OHLC file
if exists(month_OHLC_file):
  input_file = open ( month_OHLC_file,"r" )
  num_lines = sum(1 for line in open(month_OHLC_file))
else:
  print month_OHLC_file+" is NOT exist."
  sys.exit(0)

if MA:
  print MA
if MA: 
  maxMA=max(MA)
  minMA=min(MA)
#定義圖表物件
fig = plt.figure(facecolor='#07000d',edgecolor='#07000d', figsize=(15,10))
ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')

#繪製K線圖
candlestick_ohlc(ax1, OHLC, width=0.002, colorup='r', colordown='green', alpha=1)
ax1.grid(True, color='w', alpha=0.5)
ax1.axhline(y=(min(lowPrice, minMA)//100)*100,c="#5998ff" ,linewidth=0.5,zorder=0)
ax1.spines['bottom'].set_color("#5998ff")
ax1.axhline(y=(max(highPrice, maxMA)//100+1)*100,c="#5998ff" ,linewidth=0.5,zorder=0)
ax1.spines['top'].set_color("#5998ff")
ax1.spines['left'].set_color("#5998ff")
ax1.spines['right'].set_color("#5998ff")
ax1.tick_params(axis='x', colors='w')
ax1.tick_params(axis='y', colors='w')
#定義x軸時間格式
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
timeTick=OHLC[3:]
ax1.set_xticks([ line[0] for line in timeTick[::12] ])
ax1.xaxis.label.set_color("w")
plt.xlabel("Open: "+str(openprice)+" , "+"High: "+str(highPrice)+" , "+"Low: "+str(lowPrice)+" , "+"Close: "+str(closeprice))

ax1.set_yticks(np.arange((min(lowPrice, minMA)//100)*100-100, (max(highPrice, maxMA)//100)*100+100, step=20))
#ax1.set_ybound((min(lowPrice, minMA)//100)*100-100, (max(highPrice, maxMA)//100)*100+100)
ax1.get_yaxis().get_major_formatter().set_useOffset(False)
ax1.yaxis.label.set_color("w")
plt.ylabel('Futures price and Volume')

#設定兩張圖表重疊
ax2 = ax1.twinx()

#定義時間陣列、量陣列
Time= [ line[0] for line in OHLC ]
Qty= [ line[5] for line in OHLC ]

#繪製量能圖
ax2.bar(Time, Qty, color='gray', width = 0.002, alpha = 0.5,align='center')
ax2.spines['bottom'].set_color("#5998ff")
ax2.spines['top'].set_color("#5998ff")
ax2.spines['left'].set_color("#5998ff")
ax2.spines['right'].set_color("#5998ff")
ax2.tick_params(axis='x', colors='w')
ax2.tick_params(axis='y', colors='w')

#draw the MA line
if MA:
  ax1.plot_date(Time, MA, 'y-', linewidth=1)

#draw line
ax1.axhline(y=OHLC[0][1]+60,c="#ec890e",linewidth=1,zorder=0)
ax1.axhline(y=OHLC[0][1]+20,c="#42ec0e",linewidth=1,zorder=0)
ax1.axhline(y=OHLC[0][1],c="#9907A8",linewidth=1,zorder=0)
ax1.axhline(y=OHLC[0][1]-20,c="#42ec0e",linewidth=1,zorder=0)
ax1.axhline(y=OHLC[0][1]-60,c="#ec890e",linewidth=1,zorder=0)

plt.title(current_date, color="w")
plt.savefig(outputFolder+sys.argv[1].split('/')[1].split('_')[1].split('.')[0]+".png", facecolor='#07000d')
