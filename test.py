import os
tx_dir="TXfilter/"
candleStick_dir="CandleStick/"
OHLC_dir="OHLC/"
download_dir="DailyDownload/"
analyze_dir="Analyze/"
#os.system("python dailyProcessor.py %s %s %s"%(2018, 03, 27))
#os.system("python candleStick.py %sOHLC_"%(OHLC_dir)+"20180201"+".csv"+" "+OHLC_dir+"OHLC_"+"201803.csv")
#os.system("python OHLC.py %sTX_"%(tx_dir)+"20180323"+".csv")
#os.system("python TXfilter.py %s%s.csv"%(download_dir, "Daily_2018_02_05"))
os.system("python Analyze/momentum_policy.py %sOHLC_"%(OHLC_dir)+"20180425"+".csv")