# -*- coding: UTF-8 -*-
#載入相關套件及函數
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
file_name=sys.argv[1]
print ">>>>> "+os.path.basename(__file__)+" "+sys.argv[1]+" "+sys.argv[2]

'''
print os.path.basename(__file__)
print "Current Folder:"+os.getcwd()
outputFolder=sys.argv[2]
OHLCfolder=sys.argv[3]

#時間轉數值
def TimetoNumber(time):
  time=time.zfill(6)
  sec=int(time[:2])*3600+int(time[2:4])*60+int(time[4:6])
  return sec

 #數值轉時間
def NumbertoTime(sec):
 TS=str(sec%60).zfill(2)
 sec=sec/60
 TM=str(sec%60).zfill(2)
 sec=sec/60
 TH=str(sec%60).zfill(2)
 return TH+TM+TS

#設定K線初始變數
STime = TimetoNumber('084500')
ETime = TimetoNumber('134500')

#設定K線週期
Cycle = 300
OHLC=[]
lastAmount=0
lowPrice=0
highPrice=0
date=0

#取得成交資訊
fileHandle = open ( file_name,"r" )
lineList = fileHandle.readlines()
for line in lineList:
	#print line
  Input=line.replace(" ", "").split(",")
  date = Input[0]
  time = TimetoNumber(Input[3])
  price = int(Input[4])
  amount = int(Input[5])
  #calculat lowest price and highest price
  if (lowPrice==0) or (price<lowPrice):
    lowPrice=price
  if (highPrice==0) or (price>highPrice):
    highPrice=price

  if len(OHLC)==0:
    OHLC+=[[mdates.date2num(datetime.datetime.strptime(NumbertoTime(STime),"%H%M%S")),price,price,price,price,0]]
  if time<STime+Cycle:
    if price>OHLC[-1][2]:
      OHLC[-1][2]=price
    if price<OHLC[-1][3]:
      OHLC[-1][3]=price
    OHLC[-1][4]=price
  else:
    #lastAmount=amount
    if time!=ETime:
      STime+=Cycle
      print datetime.datetime.strptime(NumbertoTime(STime),"%H%M%S").time(), OHLC[-1][4]
      OHLC+=[[mdates.date2num(datetime.datetime.strptime(NumbertoTime(STime),"%H%M%S")),price,price,price,price,0]]
  OHLC[-1][5]+=amount/2
print "Lowest Price :", lowPrice, "Highest Price :", highPrice


#設定MA
MAlen = 60
MAarray = []
MA = []
MAValue = 0

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
#定義圖表物件
#fig, ax = plt.subplots()
#fig.subplots_adjust(bottom=0.2)
#定義第一張圖案在圖表的位置
#ax1 = fig.add_subplot(111)
fig = plt.figure(facecolor='#07000d',edgecolor='#07000d', figsize=(15,10))
ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
#繪製K線圖
#candlestick(ax1, OHLC, width=0.5, colorup='r', colordown='g')
candlestick_ohlc(ax1, OHLC, width=0.002, colorup='r', colordown='green', alpha=1)
ax1.grid(True, color='w', alpha=0.5)
#定義x軸時間格式
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

#ax1.yaxis.set_major_formatter(mdates.DateFormatter(')
##ax1.xaxis.set_ticks(np.arange(OHLC[0][0], OHLC[-1][0], 0.712123))
ax1.xaxis.set_major_locator(AutoDateLocator())
#delta = datetime.timedelta(minutes=15)
#ax1.set_xticks(drange(OHLC[0][0], OHLC[-1][0], delta))

ax1.yaxis.label.set_color("w")
ax1.spines['bottom'].set_color("#5998ff")
ax1.spines['top'].set_color("#5998ff")
ax1.spines['left'].set_color("#5998ff")
ax1.spines['right'].set_color("#5998ff")
ax1.tick_params(axis='y', colors='w')
#plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
ax1.tick_params(axis='x', colors='w')
plt.ylabel('Futures price and Volume')
ax1.set_yticks(np.arange((lowPrice/100)*100, (highPrice/100+1)*100+20, step=20))
timeTick=OHLC[3:]
ax1.set_xticks([ line[0] for line in timeTick[::12] ])

#設定K線圖佔圖表版面比例
#pad = 0.25
#yl = ax1.get_ylim()
#ax1.set_ylim(yl[0]-(yl[1]-yl[0])*pad,yl[1])

#設定兩張圖表重疊
ax2 = ax1.twinx()

#定義時間陣列、量陣列
Time= [ line[0] for line in OHLC ]
Qty= [ line[5] for line in OHLC ]

#繪製量能圖
ax2.bar(Time, Qty, color='gray', width = 0.002, alpha = 0.5,align='center')

#ax1v.set_ylim(0, 3*days.Volume.values.max())
ax2.spines['bottom'].set_color("#5998ff")
ax2.spines['top'].set_color("#5998ff")
ax2.spines['left'].set_color("#5998ff")
ax2.spines['right'].set_color("#5998ff")
ax2.tick_params(axis='x', colors='w')
ax2.tick_params(axis='y', colors='w')
#將量能圖定位在K線圖下方
#ax2.set_position(matplotlib.transforms.Bbox([[0.125,0.11],[0.9,0.275]]))

#ax1.set_xticks(np.arange(mdates.DateFormatter('08:45'), mdates.DateFormatter('13:50'), 20))
#plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

#for label in ax1.xaxis.get_ticklabels()[:1]:
#    label.set_visible(False)
plt.title(date, color="w")
#plt.show()
plt.savefig(outputFolder+sys.argv[1].split('/')[1].split('_')[1].split('.')[0]+".png", facecolor='#07000d')
'''