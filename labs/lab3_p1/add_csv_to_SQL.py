import mysql.connector
import sys
import pandas as pd
import numpy as np
from datetime import date
from yfinance_scraper import connect_to_MySQL_database, create_database, get_dbname_user_password, create_lookup_table, create_table, insert_to_table, add_stock_to_lookup, export_sql, handle_missing_values, calculate_daily_returns

def check_ifMultiStock(df):

	return not df.columns.levels[1].str.replace('.', '').str.isnumeric().any()
	
def flatten_multiLevelColumns(df):

	# get 2nd level of columns
	row = df.columns.get_level_values(1).values.astype('float')
	
	df.columns = df.columns.get_level_values(0)
	
	# add it and sort it to add it to the first row
	df.loc[-1] = row
	df.index = df.index + 1
	df = df.sort_index()
	
	return df

#~~~~~~~~~~~~ main() ~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':

	# read the csv file
	csv_fname = input('Please input the csv file to be inserted to SQL server:\nPlease input without .csv\n')
	csv_fname = csv_fname + '.csv'
	df = pd.read_csv(csv_fname, header = [0,1])

	multi = check_ifMultiStock(df)


	db_name, user, password = get_dbname_user_password()

	create_database(db_name, user, password)

	# connect to the database
	con = connect_to_MySQL_database(db_name, user, password)
	cursor = con.cursor()

	# create lookup table if not exist
	create_lookup_table(cursor)



	# check if dataset is multiStock or just one stock
	multiStock_flag = check_ifMultiStock(df)

	if multiStock_flag:
		# swap column levels
		df.columns = df.columns.swaplevel()

		# for each stock, make a new table
		for stock in df.columns.unique(0):

			sub_df = df.loc[:, stock]

			sub_df = handle_missing_values(sub_df)
			sub_df = calculate_daily_returns(sub_df)

			create_table(cursor, stock)
			con.commit()	
			insert_to_table(cursor, stock, sub_df)
			con.commit()
			add_stock_to_lookup(cursor, stock)
			con.commit()
	else:

		df = flatten_multiLevelColumns(df)
		stock = input('Please enter stock symbol in format XXXX:\nFor Ex: GOOG\n')

		df = handle_missing_values(df)
		df = calculate_daily_returns(df)
		
		create_table(cursor, stock)
		con.commit()	
		insert_to_table(cursor, stock, df)
		con.commit()
		add_stock_to_lookup(cursor, stock)
		con.commit()
		
	# close connection
	con.close()
