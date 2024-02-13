import pandas as pd
import mysql.connector

# get data
def get_user_password():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'
    password = input("Please enter your MySQL password:\n")
    return user, password

host = 'localhost'
user, password = get_user_password()
#database = input("Please enter your MySQL database:\n")
database = 'lab4'

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

print(df['title'])