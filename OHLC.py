# -*- coding: UTF-8 -*-
#import section
import numpy as np
import datetime
import os
import sys
import matplotlib.dates as mdates
from os.path import exists

#variables
Cycle = 300
OHLC=[]
lastAmount=0
lowPrice=0
highPrice=0
date=0

#argument
file_name=sys.argv[1]
outputFolder=sys.argv[2]
output_file_name="OHLC"+"_"+file_name.split("_")[1].split(".")[0]+".csv"

#functions
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

#process begin
print os.path.basename(__file__)
print "Current Folder:"+os.getcwd()
output_file = open(outputFolder+output_file_name,'w')
#calculate start time and end time
STime = TimetoNumber('084500')
ETime = TimetoNumber('134500')

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
      #print datetime.datetime.strptime(NumbertoTime(STime),"%H%M%S").time(), OHLC[-1][4]
      OHLC+=[[mdates.date2num(datetime.datetime.strptime(NumbertoTime(STime),"%H%M%S")),price,price,price,price,0]]
  OHLC[-1][5]+=amount/2
print "Lowest Price :", lowPrice, "Highest Price :", highPrice

for data in OHLC:
  line=str(mdates.num2date(data[0]).time())+" "+str(data[1])+" "+str(data[2])+" "+str(data[3])+" "+str(data[4])+" "+str(data[5])+"\n"
  output_file.write(line)