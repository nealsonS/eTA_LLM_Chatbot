from read_mysql_data import *
import matplotlib.pyplot as plt


def SMA(close_data, window_size): 
#simple moving average takes Close of 5 recent days and calculates average
	df = pd.DataFrame()
	df['Close'] = close_data
	df['SMA'] = close_data.rolling(window=window_size, min_periods=1).mean()
	dates = []
	for i in range(len(df['SMA'])):
		dates.append(i)
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



#~~~~~~~~~~~~ main() ~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
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
