import os
tx_dir="TXfilter/"
candleStick_dir="CandleStick/"
OHLC_dir="OHLC/"
download_dir="DailyDownload/"
os.system("python dailyProcessor.py %s %s %s"%(2018, 03, 27))
#os.system("python candleStick.py %sTX_"%(tx_dir)+"20180326"+".csv"+" "+candleStick_dir+" "+OHLC_dir)
#os.system("python OHLC.py %sTX_"%(tx_dir)+"20180302"+".csv")
#os.system("python TXfilter.py %s%s.csv"%(download_dir, "Daily_2018_02_05"))