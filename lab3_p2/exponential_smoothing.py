from read_mysql_data import *
import matplotlib.pyplot as plt



def exp_smooth(close_data, window_size): 
#simple moving average takes Close of 5 recent days and calculates average
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



#~~~~~~~~~~~~ main() ~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
	window_size = int(input("\nEnter window size (smaller number = volatile average; bigger number = rounder average\n>>> "))
	print(window_size)
	print("\n--------------------- \nCalculating Simple Moving Average...")
	close_data = df['Close']
	exp = exp_smooth(close_data, window_size)
	print(exp.head())
	usr_inp = input("\nWould you like to view a graph of the Simple Moving Average: 'yes' or 'no'?\n>>>") 
	if usr_inp == 'yes':
		exp_smooth_plot(exp, window_size)
	else:
		print('Done!')
