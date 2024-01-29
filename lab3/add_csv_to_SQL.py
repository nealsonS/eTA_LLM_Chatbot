import mysql.connector
import sys
import pandas as pd

def create_database(cursor, db_name):
	cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_name.lower()}')

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

	# get list of values
	list_val = f_df.values.tolist()
	
	query=f"""INSERT INTO {tb_name} 
	(AdjClose, Close, High, Low, Open, Volume) VALUES
	(%s, %s, %s, %s, %s, %s);
	"""
	cursor.executemany(query, list_val)
	
# MAIN FUNCTION

# collect password of mysql server
password = input("Please enter your MySQL password:\n")

# connect to database
# THIS ASSUMES USER IS ROOT
try:
	con = mysql.connector.connect(
		user='root', 
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

# create and use database
db_name = input('Please enter the name of the database:\n')
create_database(cursor=cursor, db_name=db_name)

# close the connection
con.close()

# create a new connection with the new database
con = mysql.connector.connect(
	user='root', 
	password=password,
	host='127.0.0.1',
	database=db_name)

# get cursor
cursor = con.cursor()

# read the csv file
csv_fname = input('Please input the csv file to be inserted to SQL server:\nPlease input in a xxx.csv format\n')
df = pd.read_csv(csv_fname, header=[0,1])

# swap column levels
df.columns = df.columns.swaplevel()

# for each stock, make a new table
for stock in df.columns.unique(0):
	
	sub_df = df.loc[:, stock]
	print(0)
	create_table(cursor, stock)
	con.commit()	
	insert_to_table(cursor, stock, sub_df)
	con.commit()

# add to MySQL server
#df.to_sql('stock_price', con, if_exists='replace', index=False)

# close connection
con.close()
