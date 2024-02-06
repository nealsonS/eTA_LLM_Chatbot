from read_mysql_data import *
import matplotlib.pyplot as plt



def exp_smooth(close_data, window_size): 
#exponential smoothing / moving average takes Close of 5 recent days and calculates average + considers other stuff
	df = pd.DataFrame()
	df['Close'] = close_data
	df['ExpSmooth'] = close_data.ewm(span=window_size, adjust=False).mean()
	dates = []
	for i in range(len(df['ExpSmooth'])):
		dates.append(i)  #dummy dates for now
	df['Date'] = dates
	return df



def exp_smooth_plot(data, window_size):
	plt.figure(figsize=(10, 6))
	plt.plot(data['Date'], data['Close'], label='Original Data', marker='o')
	plt.plot(data['Date'], data['ExpSmooth'], label=f'Exponential Smoothing (Window={window_size})', linestyle='--', color='red')
	plt.title('Stock Price Data with Exponential Smoothing')
	plt.xlabel('Date')
	plt.ylabel('Close Price')
	plt.legend()
	plt.show()
	
	
	
def exp_cross(close_data, short_window, long_window):
	df = pd.DataFrame()
	df['Close'] = close_data
	dates = []
	for i in range(len(df['Close'])):
		dates.append(i)  #dummy dates for now
	df['Date'] = dates
	df['Short_Term'] = df['Close'].ewm(alpha=short_window, adjust=False).mean()
	df['Long_Term'] = df['Close'].ewm(alpha=long_window, adjust=False).mean()
	df['Signal'] = 0  # 0 represents no signal
	df.loc[df['Short_Term'] > df['Long_Term'], 'Signal'] = 1 # BUY signal happens when short-term crosses above long-term
	df.loc[df['Short_Term'] < df['Long_Term'], 'Signal'] = -1 # SELL signal happens when short-term crosses below long-term
	return df
	


def exp_cross_plot(data, short_window, long_window):
	plt.plot(data['Date'], data['Close'], label='Original Data', marker='o')
	plt.plot(data['Date'], data['Short_Term'], label=f'Short-term Smoothed ({short_window})', linestyle='--', color='purple')
	plt.plot(data['Date'], data['Long_Term'], label=f'Long-term Smoothed ({long_window})', linestyle='--', color='orange')
	buy_signals = data[data['Signal'] == 1]
	plt.scatter(buy_signals['Date'], buy_signals['Short_Term'], marker='^', color='green', label='Buy Signal')
	sell_signals = data[data['Signal'] == -1]
	plt.scatter(sell_signals['Date'], sell_signals['Short_Term'], marker='v', color='red', label='Sell Signal')
	plt.title('Exponential Smoothing with Crossover Strategy')
	plt.xlabel('Date')
	plt.ylabel('Value')
	plt.legend()
	plt.show()




#~~~~~~~~~~~~ main() ~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
	close_data = df['Close']
	mode = input("\n\n1. Demo Exponential Smoothing or 2. Get BUY/SELL signals?\n>>> ")
	if mode == "1":
		window_size = int(input("\nEnter window size (smaller number = volatile average; bigger number = rounder average\n>>> "))
		print(window_size)
		print("\n--------------------- \n Doing Exponential Smoothing...")
		exp = exp_smooth(close_data, window_size)
		print(exp.head())
		usr_inp = input("\nWould you like to view a graph of the Exponential Smoothing: 'yes' or 'no'?\n>>> ") 
		if usr_inp == 'yes':
			exp_smooth_plot(exp, window_size)
		else:
			print('Done!')
	elif mode == "2":
		short_window = float(input("\nEnter a small window size (ie. 0.2)\n>>> "))
		long_window = float(input("\nEnter a big window size (ie. 0.05)\n>>> "))
		exp = exp_cross(close_data, short_window, long_window)
		print(exp.head())
		usr_inp = input("\nWould you like to view a graph of the Exponential Smoothing: 'yes' or 'no'?\n>>> ") 
		if usr_inp == 'yes':
			exp_cross_plot(exp, short_window, long_window)
		else:
			print('Done!')
		
		
		
