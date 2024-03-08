import os
import re
import sys
import PyPDF2
from PyPDF2 import PdfReader
import pytesseract
from ocrmypdf import ocr
import mysql.connector
from mysql.connector import errorcode



# Get MySQL username and password
def get_user_password():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'  # Defaults to 'root' if left blank
    password = input("Please enter your MySQL password:\n")
    return user, password



# Establish MySQL connection
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



# Extract text content from PDF
def extract_text_from_pdf(pdf_path):
    try:
        pdf_file = open(pdf_path, 'rb')
        reader = PyPDF2.PdfReader(pdf_file)
        text_pages = []
        for page in reader.pages:
            try:
                text_pages.append(str(page.extract_text() + " "))
            except KeyError:
                print(f"Skipping a page in {pdf_path} due to extraction issues.")
        for page in range(len(text_pages)):
            print("PAGE", page, "-------", text_pages[page])   
        return text_pages
    finally:
        pdf_file.close()



# have text column and image column?
def parse_details(page, text_page):
    details = {
        "page": "Unknown",
        "text_content": "Unknown",
        #"longitude": "Unknown",
        #"latitude": "Unknown",
        #"address": "Unknown"
    }
    details["page"] = str(page)
    details["text_content"] = text_page
    print(details["page"])
    return details



# Create MySQL table in database
def check_and_create_table(cursor):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cookbook (
        id INT AUTO_INCREMENT PRIMARY KEY,
        page VARCHAR(255),
        text_content TEXT
    )
    """
    cursor.execute(create_table_sql)



# Insert data into database
def insert_data_into_db(cursor, details):
    check_and_create_table(cursor)  # Ensure table exists
    insert_sql = """
    INSERT INTO cookbook (page, text_content) 
    VALUES (%s, %s)
    """
    cursor.execute(insert_sql, (details["page"], details["text_content"]))
    


# Combine all scripts
def main():
    host = 'localhost'
    #user = 'root'
    #password = ''
    #database = 'demo'  
    user, password = get_user_password()
    database = input("Please enter your MySQL database:\n")
    connection = connect_to_database(host, user, password, database)
    cursor = connection.cursor()  
    
   #get_pdf_text('./')
    pdf_directory = '/home/vboxuser/0/lab6/drive'
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)
            extracted_text = extract_text_from_pdf(pdf_path)
            print(f"Extracted for '{filename}'")
            
            for e in range(len(extracted_text)):
            	details = parse_details(e, extracted_text[e])
            	insert_data_into_db(cursor, details)
    print(f"Uploaded to '{database}' database")
    
    connection.commit()
    cursor.close()
    connection.close()



if __name__ == '__main__':
    main()
