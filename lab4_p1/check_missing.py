import mysql.connector
import pandas as pd

host = "localhost"
user = "root"
password = "" # change
database = "lab4_v2" # change

connection = mysql.connector.connect(
	host=host,
	user=user,
	password=password,
	database=database
)

cursor = connection.cursor()

table_name = "reddit_posts"
content_check = "content"
corresponding_url = "url"

# check if values are empty / "missing"
#select_query = f"SELECT * FROM {table_name} WHERE {content_check} = '' " # IS NULL would not work
select_query = f"SELECT {content_check}, {corresponding_url} FROM {table_name} WHERE {content_check} = ''"

df = pd.DataFrame()



try:
	cursor.execute(select_query)
	result = cursor.fetchall()
	if result:
     	print(f"Values in '{content_check}' that are empty and their corresponding values in '{corresponding_url}':")
     	for row in result:
        	print(f"{row[0]} : {row[1]}")
     	df = pd.DataFrame(result, columns=[content_check, corresponding_url])
     	print(df)
	else:
    	print(f"All values in column '{content_check}' are not NULL.")
except mysql.connector.Error as err:
	print(f"Error: {err}")

cursor.close()
connection.close()



#print(df)
urls = df['url']
print(urls)
