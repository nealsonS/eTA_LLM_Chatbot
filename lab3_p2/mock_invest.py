from read_mysql_data import *
import pickle
from  signal_gen import SMA_cross
import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy as np


def get_invest_duration():
	invest_duration = input('Please input how LONG should the mock investment be (in days):\nE.X: 30\n').strip()

	while not invest_duration.isnumeric():
		print('Invalid input! Please input a number!\n')
		invest_duration = input('Please input how LONG should the mock investment be (in days):\nE.X: 30\n').strip()

	return int(invest_duration)

def get_invest_amount():
	invest_amount = input('Please input how MUCH should the initial mock investment be:\nE.X: 20000\n').strip()

	while not invest_amount.isnumeric():
		print('Invalid input! Please input a number!\n')
		invest_amount = input('Please input how MUCH should the initial mock investment be:\nE.X: 20000\n').strip()

	return int(invest_amount)

def get_num_of_invest():
	invest_num = input('Please input how many shares to buy/sell each time:\nE.X: 5\n').strip()

	while not invest_num.isnumeric():
		print('Invalid input! Please input a number!\n')
		invest_num = input('Please input how many shares to buy/sell each time:\nE.X: 5\n').strip()

	return int(invest_num)

def plot_predictions(pred, ci_df):
	# Plot actual vs predicted prices
	plt.figure(figsize=(12, 6))
	plt.plot(pred, label='Predicted Stock Prices')
	plt.fill_between(ci_df.index, ci_df['Long_Term'], ci_df['Short_Term'], color='grey', alpha=0.3)
	plt.title('Predicted Stock Prices')
	plt.xlabel('Date')
	plt.ylabel('Closing Price')
	plt.legend()
	plt.show()

def perform_invest(mod, data, inv_amnt, inv_dur, inv_num):
	# create portfolio 
	p_hist = pd.DataFrame(columns = ['Close', 'Action', 'Num_shares', 'Shares_used', 'Portfolio_value', 'Amount_left'])

	train_size = int(len(data) * 0.8)
	train, test = data[:train_size], data[train_size:]

	while inv_dur > test.shape[0]:
		print(f'Invest duration is too long! Make it less than {test.shape[0]}')
		inv_dur = get_invest_duration()

	actual = test[:inv_dur]
	pred = mod.predict(n_periods = inv_dur)

	short_window = int(input("Enter a small window size (ie. 5)\n>>> "))
	long_window = int(input("Enter a big window size (ie. 20)\n>>> "))

	# generate buy/sell signals
	signal_df = SMA_cross(pred, short_window, long_window)

	# simulation code
	amt_left = inv_amnt
	action = 'Hold'
	num_shares = 0

	port_val = 0

	for i, close in enumerate(actual):
		sig_row = signal_df.iloc[i]

		signal = sig_row['Signal']
		shares_used = 0
		amt_used = 0

		# if buy signal
		if signal == 1:

			# if there is enough money to buy shares
			if amt_left >= close:
				action = 'Buy'
				
				if amt_left // close >= inv_num:
					shares_used = inv_num

				else:
					shares_used = amt_left // close

				amt_used = shares_used * close
				num_shares = num_shares + shares_used
				amt_left = amt_left - amt_used

			# if not
			else:
				action = 'Hold'

		elif signal == 0:

			# if num_shares < 0
			if num_shares <= 0:
				action = 'Hold'

			elif num_shares > 0:
				action = 'Sell'


				if num_shares >= inv_num:
					shares_used = inv_num
				else:
					shares_used = num_shares // inv_num

				amt_used = shares_used * close
				num_shares = num_shares - shares_used
				amt_left = amt_left + amt_used

		port_val = num_shares * close
		row = (close, action, num_shares, shares_used, port_val, amt_left)
		p_hist.loc[len(p_hist)] = row

	return p_hist

def calc_port_val(data):
	last_row = data.loc[len(data) - 1]
	return last_row['Amount_left'] + last_row['Portfolio_value']

def calc_total_ROI(data):
	init_inv = data.iloc[0]['Amount_left'] + data.iloc[0]['Portfolio_value']
	last_inv = data.iloc[data.shape[0]-1]['Amount_left'] + data.iloc[data.shape[0]-1]['Portfolio_value']
	roi = (last_inv-init_inv)/ init_inv * 100
	return round(roi, 2)

def calc_annual_return(data, div_val):
	years = len(data) / div_val
	init_inv = data.iloc[0]['Amount_left'] + data.iloc[0]['Portfolio_value']
	last_inv = data.iloc[data.shape[0]-1]['Amount_left'] + data.iloc[data.shape[0]-1]['Portfolio_value']

	return round((((last_inv/init_inv)**years) - 1) * 100, 2)

def calc_profit(data):
	init_inv = data.iloc[0]['Amount_left'] + data.iloc[0]['Portfolio_value']
	last_inv = data.iloc[data.shape[0]-1]['Amount_left'] + data.iloc[data.shape[0]-1]['Portfolio_value']
	return round(last_inv-init_inv, 2)

def calc_sharpe_ratio(data):
	daily_returns = data['Close'].pct_change()
	rof_rate = 0.001 #assume 0.001
	sr = (np.mean(daily_returns) - rof_rate) / daily_returns.std() * 100
	return round(sr, 2)

def get_time_interval():
	m_str = input('What interval is the dataset?\nType: daily/monthly/yearly\n').lower().strip()
	m = 1

	while m_str not in ['daily', 'monthly', 'yearly']:
		print('Invalid input!')
		m_str = input('What interval is the dataset?\nType: daily/monthly/yearly\n').lower().strip()

		div_str = ''
	if m_str == 'daily':
		div_str = '7 days'
		m = 7
	if m_str == 'monthly':
		div_str = '12 months'
		m = 12
	if m_str == 'yearly':
		div_str = '1 year'
		m = 1

	return div_str, m

if __name__ == '__main__':

	res_path = 'results/'

	data = df['Close']
	# get stock_name
	stock = table_name

	inv_dur = get_invest_duration()
	inv_amnt = get_invest_amount()
	inv_num = get_num_of_invest()
	intv_str, intv_num = get_time_interval()

	# load model
	with open(res_path + stock + '.pkl', 'rb') as f_in:
		mod = pickle.load(f_in)


	p_hist = perform_invest(mod, data, inv_amnt, inv_dur, inv_num)
	print(p_hist)
	print(f'Total Profit: {calc_profit(p_hist)}')
	print(f'Total Portfolio Value: {calc_port_val(p_hist)}')
	print(f'Total Return of Investment: {calc_total_ROI(p_hist)}')
	print(f'Annualized Returns ({intv_str}): {calc_annual_return(p_hist, intv_num)}')
	print(f'Sharpe Ratio: {calc_sharpe_ratio(p_hist)}')
	p_hist.to_csv(res_path + stock + '_hist.csv')