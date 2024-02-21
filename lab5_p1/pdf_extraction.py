import os
import sys
import PyPDF2
import pytesseract
from PIL import Image
import mysql.connector
from ocrmypdf import ocr
from mysql.connector import errorcode

# Function to get MySQL user and password
def get_user_password():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'  # Default to 'root' if left blank
    password = input("Please enter your MySQL password:\n")
    return user, password

# Establishing MySQL connection
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

# OCR PDF to Text
def ocr_pdf_to_text(pdf_path):
    output_pdf = "temp_ocr_output.pdf"
    ocr(pdf_path, output_pdf, force_ocr=True, output_type='pdf')
    reader = PyPDF2.PdfReader(output_pdf)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + " "
    os.remove(output_pdf)  # Cleanup the temporary OCR output file
    return text

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        pdf_file = open(pdf_path, 'rb')
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + " "
        if not text:
            print(f"Using OCR for: {pdf_path}")
            text = ocr_pdf_to_text(pdf_path)
        return text
    finally:
        pdf_file.close()

# Insert data into database
def insert_data_into_db(cursor, data):
    try:
        sql = "CREATE TABLE IF NOT EXISTS `Table1` (`api_number`, `longitude`, `latitude`, `well_name`, `address`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, data)
    except mysql.connector.Error as err:
        print("Failed to insert data into MySQL table:", err)

if __name__ == "__main__":
    host = 'localhost'
    user, password = get_user_password()
    database = input("Please enter your MySQL database:\n")
    
    # Connect to your database
    connection = connect_to_database(host, user, password, database)
    cursor = connection.cursor()

    # Specify the path to your PDF directory
    pdf_directory = '/home/colinzwang/Documents/DSCI560_Lab5'
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)
            extracted_text = extract_text_from_pdf(pdf_path)
            # Example data - replace with actual data extraction logic
            data = ('api_number_example', 'longitude_example', 'latitude_example', 'well_name_example', 'address_example')
            insert_data_into_db(cursor, data)

    # Commit changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()
