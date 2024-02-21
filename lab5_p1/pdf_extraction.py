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


# Extract well name and API number using flexible patterns
def extract_well_name_and_api(text):
    api_patterns = [r"API[#: ]*\s*(\d{2,}-?\d{3,}-?\d{5,})"]
    well_name_patterns = [r"Well Name and Number[: ]*\s*([\w\s]+)"]
    
    api_number = "Unknown"
    well_name = "Unknown"
    
    for pattern in api_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            api_number = match.group(1)
            break
    
    for pattern in well_name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            well_name = match.group(1).strip()
            break
    
    return well_name, api_number

# Check and create table if not exists
def check_and_create_table(cursor):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS well_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        well_name VARCHAR(255),
        api_number VARCHAR(255)
    )
    """
    cursor.execute(create_table_sql)

# Insert data into database
def insert_data_into_db(cursor, well_name, api_number):
    check_and_create_table(cursor)  # Ensure table exists
    insert_sql = "INSERT INTO well_data (well_name, api_number) VALUES (%s, %s)"
    cursor.execute(insert_sql, (well_name, api_number))

if __name__ == "__main__":
    host = 'localhost'
    user, password = get_user_password()
    database = input("Please enter your MySQL database:\n")
    
    connection = connect_to_database(host, user, password, database)
    cursor = connection.cursor()

    pdf_directory = '/home/colinzwang/Documents/DSCI560_Lab5'
    
    # Initialize counters
    count_well_name_success = 0
    count_api_success = 0
    count_failures = 0
    count_errors = 0

    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)
            try:
                extracted_text = extract_text_from_pdf(pdf_path)
                well_name, api_number = extract_well_name_and_api(extracted_text)

                if well_name != "Unknown":
                    count_well_name_success += 1
                if api_number != "Unknown":
                    count_api_success += 1
                if well_name == "Unknown" or api_number == "Unknown":
                    count_failures += 1

                print(f"Extracted for '{filename}': Well Name - {well_name}, API Number - {api_number}")

                if well_name != "Unknown" or api_number != "Unknown":
                    insert_data_into_db(cursor, well_name, api_number)
            except Exception as e:
                print(f"Error processing '{filename}': {e}")
                count_errors += 1

    connection.commit()
    cursor.close()
    connection.close()

    # Print summary
    print(f"\nSummary:")
    print(f"Total well names successfully extracted: {count_well_name_success}")
    print(f"Total API numbers successfully extracted: {count_api_success}")
    print(f"Total failures (unknown well name or API number): {count_failures}")
    print(f"Total errors during extraction: {count_errors}")

