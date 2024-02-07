import pandas as pd
import mysql.connector

def get_user_password():
    # collect password and database of mysql server
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user.lower().strip()
    if user == '':
        user = 'root'
    password = input("Please enter your MySQL password:\n")
    return user, password

host = 'localhost'
user, password = get_user_password()
database = input("Please enter your MySQL database:\n")#'lab3' #change if needed


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


