#=============================
#name:dailyProcessor.py
#argument:
#	year:2018
#	month:3
#	day:5
#author:srhuang
#email:lukyandy3162@gmail.com
#=============================

#===============
#import section
#===============
import os
from os.path import exists
import sys
import requests
import urllib 
import zipfile

#================
#variable section
#================
download_dir="DailyDownload/"
tx_dir="TXfilter/"
#candleStick_dir="CandleStick/"
root_path=os.getcwd()

#=================
#argument section
#=================
year=sys.argv[1].zfill(4)
month=sys.argv[2].zfill(2)
day=sys.argv[3].zfill(2)
file_name="Daily_"+year+"_"+month+"_"+day

#=================
#function section
#=================
def is_downloadable(url):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

#===============
#progress start
#===============
print ">>>>> "+os.path.basename(__file__)+" "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]
print "file name : "+file_name

if not exists(download_dir):
	os.makedirs(download_dir)

#download the file from server
os.chdir(download_dir)
if exists("%s.csv"%(file_name)):
	print "%s.csv is already exist."%(file_name)
else:
	url = 'http://www.taifex.com.tw/DailyDownload/DailyDownloadCSV/%s.zip'%(file_name)
	if is_downloadable(url) == True:
		urllib.urlretrieve(url, "%s.zip"%(file_name))
	else:
		print "Warning : %s is NOT on the Server."%file_name
		sys.exit(0)
	#unzip the file and remove the zip file
	with zipfile.ZipFile('%s.zip'%(file_name), 'r') as myzip:
		myzip.extract('%s.csv'%(file_name))
	os.remove('%s.zip'%(file_name))

#filter the TX
os.chdir("../")
os.system("python %s/TXfilter.py %s%s.csv"%(root_path, download_dir, file_name))
os.system("python %s/OHLC.py %s"%(root_path, tx_dir)+"TX_"+year+month+day+".csv")

print "<<<<< "+os.path.basename(__file__)+" done."
