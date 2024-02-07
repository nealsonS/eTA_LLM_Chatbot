# uses simple cross moving average to generate signal
# we will pull from this function to create signal generation
# on arima.py
import pandas as pd
def SMA_cross(close_data, short_window, long_window):
	df = pd.DataFrame()
	df['Close'] = close_data
	dates = []
	for i in range(len(df['Close'])):
		dates.append(i)  #dummy dates for now
	df['Date'] = dates
	df['Short_Term'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
	df['Long_Term'] = df['Close'].rolling(window=long_window, min_periods=1).mean()
	df['Signal'] = 0  # 0 represents no signal
	df.loc[df['Short_Term'] > df['Long_Term'], 'Signal'] = 1 # BUY signal happens when short-term crosses above long-term
	df.loc[df['Short_Term'] < df['Long_Term'], 'Signal'] = -1 # SELL signal happens when short-term crosses below long-term
	return df
	
