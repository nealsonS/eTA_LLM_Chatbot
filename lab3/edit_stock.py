import yfinance as yf
import pandas as pd
import mysql.connector

# FUNCTIONS

def get_task_input():
	task = input('Please type add/drop/display:\n')
	task = task.lower().strip()

	while task not in ['add', 'drop', 'display']:
		print('Please enter add/drop/display!\n')
		task = input('Please type add/drop/display:\n')

	return task

# scrape the stock and then add it to the MySQL server
def add_stock:



# MAIN FUNCTION

# connect to database
con = mysql.connector.connect(
	user='root', 
	password=password,
	host='127.0.0.1',
	database=db_name)
	
get_task_input
