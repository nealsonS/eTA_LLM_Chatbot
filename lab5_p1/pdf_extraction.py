import os
import re
import sys
import PyPDF2
import pytesseract
import mysql.connector
from ocrmypdf import ocr
from mysql.connector import errorcode

# Function to get MySQL user and password
def get_user_password():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'  # Defaults to 'root' if left blank
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
            try:
                text += page.extract_text() + " "
            except KeyError:
                print(f"Skipping a page in {pdf_path} due to extraction issues.")
        return text
    finally:
        pdf_file.close()


def extract_well_details(text):
    details = {
        "well_name": "Unknown",
        "api_number": "Unknown",
        "longitude": "Unknown",
        "latitude": "Unknown",
        "address": "Unknown"
    }

    # Regex patterns for new fields
    longitude_pattern = r"Longitude[: ]*\s*([-+]?\d{1,3}\.\d+)"
    latitude_pattern = r"Latitude[: ]*\s*([-+]?\d{1,3}\.\d+)"
    address_pattern = r"Address[: ]*\s*([\w\s,]+)"

    # Existing patterns for well name and API number
    api_patterns = [r"API[#: ]*\s*(\d{2,}-?\d{3,}-?\d{5,})"]
    well_name_patterns = [r"Well Name and Number[: ]*\s*([\w\s]+)"]

    # well_name_patterns = [
    #     r"Well Name(?: and Number)?[: ]*\s*([,\w\s]+?)(?= and Number|$)"
    # ]

    # Update details dict based on matches
    for name, pattern in [("longitude", longitude_pattern), ("latitude", latitude_pattern), ("address", address_pattern)]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            details[name] = match.group(1).strip()

    for pattern in api_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            details["api_number"] = match.group(1)
            break

    for pattern in well_name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            details["well_name"] = match.group(1).strip()
            break

    return details


def check_and_create_table(cursor):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS well_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        well_name VARCHAR(255),
        api_number VARCHAR(255),
        longitude VARCHAR(255),
        latitude VARCHAR(255),
        address TEXT
    )
    """
    cursor.execute(create_table_sql)

def insert_data_into_db(cursor, details):
    check_and_create_table(cursor)  # Ensure table exists
    insert_sql = """
    INSERT INTO well_data (well_name, api_number, longitude, latitude, address) 
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_sql, (details["well_name"], details["api_number"], details["longitude"], details["latitude"], details["address"]))


if __name__ == "__main__":
    host = 'localhost'
    user, password = get_user_password()
    database = input("Please enter your MySQL database:\n")
    
    connection = connect_to_database(host, user, password, database)
    cursor = connection.cursor()

    pdf_directory = '/home/colinzwang/Documents/DSCI560_Lab5'
    

    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)
            extracted_text = extract_text_from_pdf(pdf_path)
            details = extract_well_details(extracted_text)
            
            print(f"Extracted for '{filename}': {details}")
            
            if details["well_name"] != "Unknown" and details["api_number"] != "Unknown":
                insert_data_into_db(cursor, details)


    connection.commit()
    cursor.close()
    connection.close()
