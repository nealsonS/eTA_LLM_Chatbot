from multi_rake import Rake
from rake_nltk import Rake
import pandas as pd
import mysql.connector

def get_user_password():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'
    password = input("Please enter your MySQL password:\n")
    return user, password

host = 'localhost'
user, password = get_user_password()
#database = input("Please enter your MySQL database:\n")
database = 'lab4_v1'

conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cursor = conn.cursor()

query = f"SELECT title FROM reddit_posts"
cursor.execute(query)

rows = cursor.fetchall()

columns = [col[0] for col in cursor.description]

df = pd.DataFrame(rows, columns=columns)
print(df.head())
titles = df['title'] 


r = Rake()
keywords = []

for t in titles: #t should be str
	r.extract_keywords_from_text(t) # will return None. see results with get_ functions
	#r.extract_keywords_from_sentences(t) 	#for longer text
	#print(r.get_ranked_phrases())
	print(str(r.get_ranked_phrases()))
	keyword = r.get_ranked_phrases()
	keywords.append(keyword)
#	keywords.append(r.get_ranked_phrases())
	#cursor.execute("INSERT INTO reddit_posts (keywords) VALUES (%s)", (keyword))
	#print(r.get_ranked_phrases_with_scores()) 
	
	#keywords = r.apply(str(t)) # multi-rake code
	#print(keywords[:10]) # multi-rake code

#print(keywords)

# Example SQL statements to add a new column and populate it
table_name = "reddit_posts"
new_column_name = "keywords"
values_to_add = keywords  # Replace with your actual values
print(values_to_add)
print(type(values_to_add[1]))

# Execute the SQL statement to add the new column
alter_query = f"ALTER TABLE {table_name} ADD COLUMN {new_column_name} TEXT"
try:
    cursor.execute(alter_query)
    print(f"Column '{new_column_name}' added successfully.")
    connection.commit()
except mysql.connector.Error as err:
    print(f"Error: {err}")

# Execute the SQL statement to populate the values for the new column
update_query = f"UPDATE {table_name} SET {new_column_name} = %s"
data = [(value,) for value in values_to_add]

try:
    cursor.executemany(update_query, data)
    print(f"Values added to column '{new_column_name}' successfully.")
    connection.commit()
except mysql.connector.Error as err:
    print(f"Error: {err}")

# Close the cursor and connection
cursor.close()
connection.close()
