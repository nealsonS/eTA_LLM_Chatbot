import pandas as pd
import mysql.connector


host = 'localhost'
user = 'root' #change if needed
password = '' #change if needed
database = 'demo' #change if needed


connect = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cursor = connect.cursor()


query = f"SHOW TABLES"
cursor.execute(query)
for table_name in cursor:
	print(table_name)
		

table_name = input("\nWhat company data would you like to read?\n>>> ").upper()
print()
query = f"SELECT * FROM {table_name}"
cursor.execute(query)

rows = cursor.fetchall()

columns = [col[0] for col in cursor.description]

df = pd.DataFrame(rows, columns=columns)

cursor.close()
connect.close()

print(df.head())


