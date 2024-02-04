import pandas as pd
import mysql.connector

def get_dbname_user_password():
	# collect password and database of mysql server
	user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
	user = user.lower().strip()
	if user == '':
		user = 'root'
	password = input("Please enter your MySQL password:\n")
	db_name = input('Please enter the name of the database:\n')
	return db_name, user, password


# function to fetch all tables from mysql
# returns a dictionary of all the stock data for ex: {AMZN: dataframe, GOOG: dataframe}
def fetch_data(db_name, user, password):

	con = mysql.connector.connect(
		user=user, 
		password=password,
		host='127.0.0.1',
		database=db_name)

	cursor = con.cursor()

	# get table names
	cursor.execute('SHOW TABLES;')
	table_tuples = cursor.fetchall()

	# stock_lookup name
	lookup_name = 'STOCK_LOOKUP'

	# drop STOCK_LOOKUP
	table_tuples.remove((lookup_name,))

	col_names = ['AdjClose', 'Close', 'High', 'Low', 'Open', 'Volume']
	# dict of dataframes
	dict_df = {}
	# if portfolio is not empty
	if len(table_tuples) > 0:

		# get list of table names
		table_names = [name[0] for name in table_tuples]



		for table in table_names:
			# get head of stock portfolio
			cursor.execute(f"SELECT * FROM `{table}`")
			dict_df[table] = pd.DataFrame(cursor.fetchall(), columns = col_names)

	con.close()

	return dict_df

db_name, user, password = get_dbname_user_password()
dict_df = fetch_data(db_name, user, password)