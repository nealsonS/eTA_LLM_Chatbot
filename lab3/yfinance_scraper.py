import yfinance as yf
import pandas as pd
#from datetime import datetime



def user_companies():
	usr_input = input("Enter company name(s), separate by space:\n>>>")
	companies = usr_input.upper()
	return companies
	
	
def user_period():
	period_range = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max']
	message = "Enter time range from this list:\n" + str(period_range) + "\n('max' is recommended)\n>>>"
	usr_input = input(message)
	if usr_input in period_range:
		return usr_input

	
def user_interval():
	interval_range = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']
	message = "Enter interval range from this list:\n" + str(interval_range) + "\n>>>"
	usr_input = input(message)
	if usr_input in interval_range:
		return usr_input

	
#~~~~~~ from https://www.qmr.ai/yfinance-library-the-definitive-guide/#Fetch_Options_Chain_Data_from_Yahoo_Finance  ~~~~~~
def hist_scraping(companies, period, interval):
	#end_date = datetime.now().strftime('%Y-%m-%d')
	data = yf.download(companies, period=period, interval=interval)
	return data


def export_data(data_hist):
	data = data_hist
	print(data.head())
	df = pd.DataFrame(data)
	name = input("Name the output file (do not include .csv or .txt):\n>>>")
	csv_path = "./" + name + ".csv" 
	df.to_csv(csv_path, index=False)
	txt_path = "./" + name + ".txt"  #txt for easier loading to mysql
	df.to_csv(txt_path, sep='\t', index=False)
	
	
	
#~~~~~~~~~~~~ main() ~~~~~~~~~~~~~~~~~~~
stock_companies = user_companies()
print(stock_companies)
stock_period = user_period()
print(stock_period)
stock_interval = user_interval()
print(stock_interval)

data = hist_scraping(stock_companies, stock_period, stock_interval)
export_data(data)
	
	

