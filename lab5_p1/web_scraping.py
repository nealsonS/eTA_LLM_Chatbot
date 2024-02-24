import os
import re
import sys
import mysql.connector
import PyPDF2
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
        "barrels_of_oil": "VARCHAR(255)",
        "barrels_of_gas": "VARCHAR(255)"
    }
    
    # Try adding each new column without IF NOT EXISTS clause
    for column_name, column_type in new_columns.items():
        try:
            cursor.execute(f"ALTER TABLE well_data ADD COLUMN {column_name} {column_type}")
        except mysql.connector.Error as err:
            # If an error occurs, likely because the column already exists, catch and ignore the error
            # or log it if necessary
            print(f"Skipped adding {column_name}: {err.msg}")

# Get the link associated with well name for the detailed page
def get_well_detail_link(api_number):
    search_url = f"https://www.drillingedge.com/search?type=wells&api_no={api_number}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the well name link in the table
    table = soup.find('table', class_='table wide-table interest_table')
    if not table:
        print(f"Failed to find table for API number {api_number}")
        return None

    well_link = table.find('a', href=True)  # The first link is the well detail link
    if well_link:
        return well_link['href']
    else:
        print(f"Failed to find well link for API number {api_number}")
        return None

# Scrape the detailed page for required information
def fetch_well_details(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch details from {url}")
        return {}
    
    details_soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract barrels of oil as the first <span class="dropcap">
    barrels_of_oil_span = details_soup.find('span', class_='dropcap')
    barrels_of_oil = barrels_of_oil_span.text.strip() if barrels_of_oil_span else "Not available"
    
    # Extract barrels of gas as the second <span class="dropcap">
    barrels_of_gas_spans = details_soup.find_all('span', class_='dropcap')
    barrels_of_gas = barrels_of_gas_spans[1].text.strip() if len(barrels_of_gas_spans) > 1 else "Not available"
    
    
    # Extract additional details from the skinny table
    details_table = details_soup.find('table', class_='skinny')
    details = {}
    if details_table:
        for row in details_table.find_all('tr'):
            cols = row.find_all(['th', 'td'])  # Get all cells
            if len(cols) > 1:  # Ensure there's at least one key-value pair
                # Iterating over cells, considering each key-value pair
                for i in range(0, len(cols) - 1, 2):
                    key = cols[i].text.strip()
                    value = cols[i+1].text.strip()
                    details[key] = value
    
    # Extracting specific information
    well_status = details.get("Well Status", "Not available")
    well_type = details.get("Well Type", "Not available")
    closest_city = details.get("Closest City", "Not available")
    well_name = details.get("Well Name", "Not available")
    
    return {
        "barrels_of_oil": barrels_of_oil,
        "barrels_of_gas": barrels_of_gas,
        "well_status": well_status,
        "well_type": well_type,
        "closest_city": closest_city,
        "well_name": well_name
    }


# Use scraped information to update new columns in table
def update_well_in_db(cursor, api_number, well_details):
    print(f"Updating database for API {api_number} with scraped information.")
    
    # Construct the SQL update statement
    update_sql = """
    UPDATE well_data SET
        well_status = %s,
        well_type = %s,
        closest_city = %s,
        barrels_of_oil = %s,
        barrels_of_gas = %s,
        well_name = %s,
    WHERE api_number = %s
    """
    
    # Prepare the data tuple for the SQL query
    data_tuple = (
        well_details.get('well_status', 'N/A'),  # Default to 'N/A' if not found
        well_details.get('well_type', 'N/A'),
        well_details.get('closest_city', 'N/A'),
        well_details.get('barrels_of_oil', 'N/A'),
        well_details.get('barrels_of_gas', 'N/A'),
        well_details.get('well_name','N/A'),
        api_number,
    )
    
    try:
        cursor.execute(update_sql, data_tuple)
        print("Database update successful for API number:", api_number)
    except mysql.connector.Error as err:
        print(f"Error updating database for API {api_number}: {err}")

if __name__ == "__main__":
    host = 'localhost'
    user, password = get_user_password()
    database = input("Please enter your MySQL database:\n")
    
    connection = connect_to_database(host, user, password, database)
    print("Connected to the database.")
    cursor = connection.cursor()

    check_and_create_table(cursor)

    # Fetch API numbers and process each
    cursor.execute("SELECT api_number FROM well_data")
    for (api_number,) in cursor.fetchall():
        detail_page_url = get_well_detail_link(api_number)
        if detail_page_url:
            well_details = fetch_well_details(detail_page_url)
            update_well_in_db(cursor, api_number, well_details)
        else:
            print(f"No detail link found for API number {api_number}")

    connection.commit()
    cursor.close()
    connection.close()
