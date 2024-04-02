import os
import sys
import shutil
import mysql.connector
from mysql.connector import errorcode



def get_mysql():
    host = 'localhost'
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'  # Defaults to 'root' if left blank
    password = input("Please enter your MySQL password:\n")
    database = input("Please enter your MySQL database:\n")
    return host, user, password, database


def connect_to_database(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL:", err)
        sys.exit(1)
        
        
def check_and_create_table(cursor):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cookbook (
        id INT AUTO_INCREMENT PRIMARY KEY,
        doc_name VARCHAR(255),
        page VARCHAR(255),
        text_content TEXT,
        image_path VARCHAR(255)
    )
    """
    cursor.execute(create_table_sql)


def insert_data_into_db(cursor, details):
    check_and_create_table(cursor)  # Ensure table exists
    for image_path in details["image_path"]:
        insert_sql = """
        INSERT INTO cookbook (doc_name, page, text_content, image_path) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (details["doc_name"], details["page"], details["text_content"], image_path))
        
        
if __name__ == '__main__':
    #host = 'localhost'
    #user = 'root'
    #password = ''
    #database = 'demo1'
    host, user, password, database = get_mysql()
    connection = connect_to_database(host, user, password, database)
    cursor = connection.cursor()
