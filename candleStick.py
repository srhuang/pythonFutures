# -*- coding: UTF-8 -*-
#=============================
#name:candleStick.py
#argument:
# current month OHLC:csv file
# last month OHLC   :csv file
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
MAarray = []
MA = []
MAValue = 0

#=================
#argument section
#=================
current_file_name=sys.argv[1]
last_file_name=sys.argv[2]
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
    OHLC+=[[mdates.date2num(datetime.datetime.strptime(Input[0], "%H:%M:%S")), int(Input[1]), int(Input[2]), int(Input[3]), int(Input[4]), int(Input[5])]]
  line_count+=1
'''
#Calculate the MA data
if exists(last_file_name):
  input_file = open ( last_file_name,"r" )
  num_lines = sum(1 for line in open(last_file_name))
else:
  print last_file_name+" is NOT exist."
  sys.exit(0)

for i in OHLC:
  time=i[0]
  price=int(i[4])
  if len(MAarray)==0:
    MAarray+=[price]
  else:
    if time<STime+Cycle:
      MAarray[-1]=price
    else:
      if len(MAarray)==MAlen:
        MAarray=MAarray[1:]+[price]
      else:
        MAarray+=[price]   
    STime = STime+Cycle
  MAValue=float(sum(MAarray))/len(MAarray)
  print mdates.num2date(time).time(), MAValue
  #MA.extend([MAValue])
'''
#定義圖表物件
fig = plt.figure(facecolor='#07000d',edgecolor='#07000d', figsize=(15,10))
ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')

#繪製K線圖
candlestick_ohlc(ax1, OHLC, width=0.002, colorup='r', colordown='green', alpha=1)
ax1.grid(True, color='w', alpha=0.5)
ax1.spines['bottom'].set_color("#5998ff")
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

ax1.set_yticks(np.arange((lowPrice/100)*100, (highPrice/100+1)*100+20, step=20))
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

plt.title(current_date, color="w")
plt.savefig(outputFolder+sys.argv[1].split('/')[1].split('_')[1].split('.')[0]+".png", facecolor='#07000d')
