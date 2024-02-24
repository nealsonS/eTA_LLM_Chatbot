import os
import re
import sys
import mysql.connector
import PyPDF2
from ocrmypdf import ocr
from mysql.connector import errorcode
import requests
from bs4 import BeautifulSoup

def get_user_password():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'
    password = input("Please enter your MySQL password:\n")
    return user, password

def connect_to_database(host, user, password, database):
    try:
        return mysql.connector.connect(host=host, user=user, password=password, database=database)
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        sys.exit(1)

def check_and_create_table(cursor):
    # Ensure the basic structure of the table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS well_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            well_name VARCHAR(255),
            api_number VARCHAR(255),
            longitude VARCHAR(255),
            latitude VARCHAR(255),
            address TEXT
        )
    """)

    # New or additional columns to be added
    new_columns = {
        "well_status": "VARCHAR(255)",
        "well_type": "VARCHAR(255)",
        "closest_city": "VARCHAR(255)",
        "barrels_of_oil": "VARCHAR(255)"
    }
    
    # Try adding each new column without IF NOT EXISTS clause
    for column_name, column_type in new_columns.items():
        try:
            cursor.execute(f"ALTER TABLE well_data ADD COLUMN {column_name} {column_type}")
        except mysql.connector.Error as err:
            # If an error occurs, likely because the column already exists, catch and ignore the error
            # or log it if necessary
            print(f"Skipped adding {column_name}: {err.msg}")


def scrape_well_info(api_number):
    search_url = f"https://www.drillingedge.com/search?type=wells&api_no={api_number}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table by class (adjust class name as needed based on actual page structure)
    table = soup.find('table', class_='wide-table interest_table')
    well_info = {}

    if table:
        # Assuming first <tr> is the header and the next <tr> contains the desired data
        data_rows = table.find_all('tr')[1:]  # Skip header row

        for row in data_rows:
            # Extracting table data. Adjust as per actual HTML structure
            cols = row.find_all('td')
            well_info = {
                "api": cols[0].text.strip(),
                "well_name": cols[1].text.strip(),
                "lease_name": cols[2].text.strip(),
                "location": cols[3].text.strip(),
                "operator": cols[4].text.strip(),
                "status": cols[5].text.strip(),
            }
            break  
            
    return well_info

def update_well_in_db(cursor, well_info):
    update_sql = """
    UPDATE well_data SET
        well_name = %s, lease_name = %s, location = %s,
        operator = %s, status = %s
    WHERE api_number = %s
    """
    cursor.execute(update_sql, (
        well_info["well_name"], well_info["lease_name"], well_info["location"],
        well_info["operator"], well_info["status"], well_info["api"]
    ))


if __name__ == "__main__":
    host = 'localhost'
    user, password = get_user_password()
    database = input("Please enter your MySQL database:\n")
    
    connection = connect_to_database(host, user, password, database)
    cursor = connection.cursor()
    
    check_and_create_table(cursor)
    
    cursor.execute("SELECT api_number FROM well_data")
    apis = cursor.fetchall()
    
    for (api_number,) in apis:
        well_info = scrape_well_info(api_number)
        if well_info:
            update_well_in_db(cursor, well_info)
            print(f"Updated database for API {api_number}.")


    connection.commit()
    cursor.close()
    connection.close()
