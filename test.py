import os
tx_dir="TXfilter/"
candleStick_dir="CandleStick/"
OHLC_dir="OHLC/"
#os.system("python dailyProcessor.py %s %s %s"%(2018, 03, 21))
#os.system("python candleStick.py %sTX_"%(tx_dir)+"20180326"+".csv"+" "+candleStick_dir+" "+OHLC_dir)
os.system("python OHLC.py %sTX_"%(tx_dir)+"20180326"+".csv"+" "+OHLC_dir)