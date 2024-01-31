import yfinance as yf
import pandas as pd
import sys
import numpy as np
import mysql.connector
from datetime import date

def user_companies():

	validated = False
	companies_list = []

	while not validated:
		info = None
		usr_input = input("Enter company name(s), separate by space:\n>>>")
		companies = usr_input.upper().strip()
		companies_list = companies.split()

		# I noticed that the info of stocks that aren't in yticker has info that is: {'trailingPegRatio': None}
		for stock in companies_list:
			ticker = yf.Ticker(stock)
			info = ticker.info
			if info == {'trailingPegRatio': None}:
				print(f"\nStock {stock} is not available in yfinance!\nPlease enter one that does")
				break
		else:
			validated = True
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

def get_output_format():
	output = input('Please type csv to export to a csv and txt file\nPlease type sql to add it to sql server\n:')
	output = output.lower().strip()

	return output

def export_data(data_hist):
	data = data_hist
	print(data.head())
	df = pd.DataFrame(data)
	name = input("Name the output file (do not include .csv or .txt):\n>>>")
	csv_path = "./" + name + ".csv" 
	df.to_csv(csv_path, index=False)
	txt_path = "./" + name + ".txt"  #txt for easier loading to mysql
	df.to_csv(txt_path, sep='\t', index=False)

	print(f'Exported as {name}.csv and {name}.txt!')


#~~~~~~ FUNCTIONS TO ADD TO MySQL server ~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_dbname_user_password():
	# collect password and database of mysql server
	user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
	user = user.lower().strip()
	if user == '':
		user = 'root'
	password = input("Please enter your MySQL password:\n")
	db_name = input('Please enter the name of the database:\n')
	return db_name, user, password

def create_database(db_name, user, password):

	# connect to database
	# THIS ASSUMES USER IS ROOT
	try:
		con = mysql.connector.connect(
			user=user, 
			password=password,
			host='127.0.0.1')
			
	# if connection has problem (Error Handling):
	# from: https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
			
		# stop the program
		sys.exit("Connection Error! Stopping program...")

	# get cursor to execute queries on database
	cursor = con.cursor()

	cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_name.lower()}')

	# close the connection
	con.close()

def connect_to_MySQL_database(db_name, user, password):
	# THIS ASSUMES USER IS ROOT
	con = mysql.connector.connect(
		user=user, 
		password=password,
		host='127.0.0.1',
		database=db_name)

	return con

def create_lookup_table(cursor):
	q1 = """CREATE TABLE IF NOT EXISTS STOCK_LOOKUP(
		Stock VARCHAR(4), 
		CreationDate VARCHAR(10), 
		PRIMARY KEY (Stock)
		);"""
		
	cursor.execute(q1)

def create_table(cursor, tb_name):
	d_query=f"DROP TABLE IF EXISTS {tb_name};"
	c_query=f"""CREATE TABLE {tb_name}(
	AdjClose FLOAT,
	Close FLOAT,
	High FLOAT,
	Low FLOAT,
	Open FLOAT,
	Volume FLOAT
	);
	"""
	cursor.execute(d_query)
	cursor.execute(c_query)

def insert_to_table(cursor, tb_name, f_df):
	
	# convert to None to avoid loading in NumPy
	f_df = f_df.where(pd.notna(f_df), None)
	
	# list of values
	val_arr = np.array(f_df.values.tolist())
	
	# convert np.nan to None
	val_arr_None = [[None if np.isnan(val) else val for val in row] for row in val_arr]
	
	query=f"""INSERT INTO {tb_name} 
	(AdjClose, Close, High, Low, Open, Volume) VALUES
	({', '.join(['%s' for i in f_df.columns])});
	"""
	
	cursor.executemany(query, val_arr_None)

def add_stock_to_lookup(cursor, tb_name):
	
	# get today's date
	today = date.today().strftime('%Y-%m-%d')
	q1 = f'INSERT INTO STOCK_LOOKUP (Stock, CreationDate) VALUES ("{tb_name}", "{today}");'
	
	# to skip if already exists
	try:
		cursor.execute(q1)
	except mysql.connector.errors.IntegrityError as err:
		pass

def export_sql(data_hist, stock_str, db_name, user, password):
	data = data_hist
	print(data.head())
	df = pd.DataFrame(data)


	create_database(db_name, user, password)

	# connect to the database
	con = connect_to_MySQL_database(db_name, user, password)
	cursor = con.cursor()

	# create lookup table if not exist
	create_lookup_table(cursor)

	multi = len(stock_str.split(' ')) > 1

	if multi:
		# swap column levels
		df.columns = df.columns.swaplevel()

		# for each stock, make a new table
		for stock in df.columns.unique(0):

			sub_df = df.loc[:, stock]
			create_table(cursor, stock)
			con.commit()	
			insert_to_table(cursor, stock, sub_df)
			con.commit()
			add_stock_to_lookup(cursor, stock)
			con.commit()
	else:
		
		stock = stock_str
		create_table(cursor, stock)
		con.commit()	
		insert_to_table(cursor, stock, df)
		con.commit()
		add_stock_to_lookup(cursor, stock)
		con.commit()
		
	# close connection
	con.close()
	print('Added to MySQL server!')

	
#~~~~~~~~~~~~ main() ~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
	stock_companies = user_companies()
	print(stock_companies)
	stock_period = user_period()
	print(stock_period)
	stock_interval = user_interval()
	print(stock_interval)

	data = hist_scraping(stock_companies, stock_period, stock_interval)

	print('Data scraped!')

	output_format = get_output_format()

	if output_format == 'csv':
		export_data(data)
	elif output_format== 'sql':
		db_name, user, password = get_dbname_user_password()
		export_sql(data, stock_companies, db_name, user, password)



	

