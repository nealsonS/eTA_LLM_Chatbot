import yfinance as yf
import pandas as pd
import mysql.connector
# import from Deborah's code
from yfinance_scraper import *

# FUNCTIONS

def get_task_input():
	task = input('Please type add/drop/display or end to stop the program:\n')
	task = task.lower().strip()

	while task not in ['add', 'drop', 'display', 'end']:
		print('Please enter add/drop/display!')
		task = input('Please type add/drop/display or end to stop the program::\n')

	return task

# scrape the stock and then add it to the MySQL server
def add_stock(db_name, user, password):
	stock_companies = user_companies()
	print(stock_companies)
	stock_period = user_period()
	print(stock_period)
	stock_interval = user_interval()
	print(stock_interval)

	data = hist_scraping(stock_companies, stock_period, stock_interval)
	data = handle_missing_values(data)
	data = calculate_daily_returns(data)

	export_sql(data, stock_companies, db_name, user, password)

def display_stock(db_name, user, password):

	con = connect_to_MySQL_database(db_name, user, password)
	cursor = con.cursor()

	# get table names
	cursor.execute('SHOW TABLES;')
	table_tuples = cursor.fetchall()

	# stock_lookup name
	lookup_name = 'STOCK_LOOKUP'

	# drop STOCK_LOOKUP
	table_tuples.remove((lookup_name,))

	col_names = ['AdjClose', 'Close', 'High', 'Low', 'Open', 'Volume']

	# if portfolio is not empty
	if len(table_tuples) > 0:

		# get list of table names
		table_names = [name[0] for name in table_tuples]

		for table in table_names:
			# get head of stock portfolio
			cursor.execute(f"SELECT * FROM `{table}` LIMIT 5")
			print(f'\nStock: {table}\nBelow is the top 5 rows:\n')
			print(pd.DataFrame(cursor.fetchall(), columns = col_names))

			# get creation date from stock lookup table
			cursor.execute(f"SELECT `CreationDate` FROM `{lookup_name}` WHERE `Stock` = '{table}'")

			# to unlist it
			creation_date = [date[0] for date in cursor.fetchall()][0]
			print(f'\nThe creation date is: {creation_date}\n')

	else:
		print("No stocks in portfolio!")


	con.close()




def drop_stock(db_name, user, password):

	con = connect_to_MySQL_database(db_name, user, password)
	cursor = con.cursor()

	stock = input('Please enter stock symbol to drop with spaces in format XXXX XXXX:\nFor Ex: GOOG AMZN\n')
	stock_list = stock.strip().upper().split(' ')


	for stock in stock_list:
		query_drop_table = f'DROP TABLE IF EXISTS {stock}'
		query_drop_lookup = f"DELETE FROM `STOCK_LOOKUP` WHERE `Stock` = '{stock}'"
		cursor.execute(query_drop_table)
		con.commit()
		cursor.execute(query_drop_lookup)
		con.commit()

		print(f'Dropped {stock} from portfolio!')

	con.close()
	
def handle_missing_values(df):
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    return df

def calculate_daily_returns(df):
    df['Daily_Returns'] = df['Close'].pct_change()
    return df


#~~~~~~~~~~~~ main() ~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':

	task = get_task_input()

	if task != 'end':
		print('Disclaimer: You will input this only once!\n')
		db_name, user, password = get_dbname_user_password()

	while task != 'end':

		if task == 'add':
			add_stock(db_name, user, password)
		elif task == 'drop':
			drop_stock(db_name, user, password)
		elif task == 'display':
			display_stock(db_name, user, password)

		task = get_task_input()


