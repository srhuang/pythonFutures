import os
from os.path import exists
import sys
import requests

file_name="Daily_"+sys.argv[1]+"_"+sys.argv[2].zfill(2)+"_"+sys.argv[3].zfill(2)
print "file name : "+file_name

download_dir="DailyDownload/"
tx_dir="TXfilter/"
OHLC_dir="OHLC/"
candleStick_dir="CandleStick/"
root_path=os.getcwd()

def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

if not exists(download_dir):
	os.makedirs(download_dir)
if not exists(tx_dir):
	os.makedirs(tx_dir)
if not exists(candleStick_dir):
	os.makedirs(candleStick_dir)

os.chdir(download_dir)

if exists("%s.csv"%(file_name)):
	print "%s.csv is already exist."%(file_name)
else:
	import urllib 
	url = 'http://www.taifex.com.tw/DailyDownload/DailyDownloadCSV/%s.zip'%(file_name)
	#print "downloading with urllib"
	if is_downloadable(url) == True:
		urllib.urlretrieve(url, "%s.zip"%(file_name))
	else:
		print "ERROR : %s is NOT on the Server."%file_name
		sys.exit(0)

	import zipfile
	with zipfile.ZipFile('%s.zip'%(file_name), 'r') as myzip:
		myzip.extract('%s.csv'%(file_name))
	os.remove('%s.zip'%(file_name))

os.chdir("../")
test=file_name.split('_')
if exists(tx_dir+"TX_"+test[1]+test[2]+test[3]+".csv"):
	print "TX_"+test[1]+test[2]+test[3]+".csv is already exist."
else:
	os.system("python %s/TXfilter.py %s%s.csv"%(root_path, download_dir, file_name)+" "+tx_dir)

if exists(OHLC_dir+"OHLC_"+test[1]+test[2]+test[3]+".csv"):
	print "OHLC_"+test[1]+test[2]+test[3]+".csv is already exist."
else:
	os.system("python %s/OHLC.py %s"%(root_path, tx_dir)+"TX_"+test[1]+test[2]+test[3]+".csv"+" "+OHLC_dir)


