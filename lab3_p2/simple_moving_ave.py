from read_mysql_data import *
import matplotlib.pyplot as plt


def SMA(close_data, window_size): 
#simple moving average takes Close of 5 recent days and calculates average
	df = pd.DataFrame()
	df['Close'] = close_data
	df['SMA'] = close_data.rolling(window=window_size, min_periods=1).mean()
	dates = []
	for i in range(len(df['SMA'])):
		dates.append(i)  #dummy dates for now
	df['Date'] = dates
	return df


def SMA_plot(data, window_size):
	plt.figure(figsize=(10, 6))
	plt.plot(data['Date'], data['Close'], label='Original Data', marker='o')
	plt.plot(data['Date'], data['SMA'], label=f'{window_size}-Point Moving Average', linestyle='--', color='red')
	plt.title('Stock Price with Moving Average')
	plt.xlabel('Date')
	plt.ylabel('Close Price')
	plt.legend()
	plt.show()



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
	


def SMA_cross_plot(data, short_window, long_window):
	plt.plot(data['Date'], data['Close'], label='Original Data', marker='o')
	plt.plot(data['Date'], data['Short_Term'], label=f'Short-term Smoothed ({short_window})', linestyle='--', color='purple')
	plt.plot(data['Date'], data['Long_Term'], label=f'Long-term Smoothed ({long_window})', linestyle='--', color='orange')
	buy_signals = data[data['Signal'] == 1]
	plt.scatter(buy_signals['Date'], buy_signals['Short_Term'], marker='^', color='green', label='Buy Signal')
	sell_signals = data[data['Signal'] == -1]
	plt.scatter(sell_signals['Date'], sell_signals['Short_Term'], marker='v', color='red', label='Sell Signal')
	plt.title('Simple Moving Average with Crossover Strategy')
	plt.xlabel('Date')
	plt.ylabel('Value')
	plt.legend()
	plt.show()
	


#~~~~~~~~~~~~ main() ~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
	close_data = df['Close']
	mode = input("\n\n1. Demo Simple Moving Average or 2. Get BUY/SELL signals?\n>>> ")
	if mode == "1":
		window_size = int(input("\nEnter window size (smaller number = volatile average; bigger number = rounder average\n>>> "))
		print(window_size)
		print("\n--------------------- \nCalculating Simple Moving Average...")
		close_data = df['Close']
		sma = SMA(close_data, window_size)
		print(sma.head())
		usr_inp = input("\nWould you like to view a graph of the Simple Moving Average: 'yes' or 'no'?\n>>>") 
		if usr_inp == 'yes':
			SMA_plot(sma, window_size)
		else:
			print('Done!')
	elif mode == "2":
		short_window = int(input("\nEnter a small window size (ie. 5)\n>>> "))
		long_window = int(input("\nEnter a big window size (ie. 20)\n>>> "))
		sma = SMA_cross(close_data, short_window, long_window)
		print(sma.head())
		usr_inp = input("\nWould you like to view a graph of the Simple Moving Average: 'yes' or 'no'?\n>>> ") 
		if usr_inp == 'yes':
			SMA_cross_plot(sma, short_window, long_window)
		else:
			print('Done!')
		
		
		
