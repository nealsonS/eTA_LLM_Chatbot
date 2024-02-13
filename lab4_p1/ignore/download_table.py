import csv
from data_collection import get_user_password
import mysql.connector


def download_table_to_file(filename):
    """
    Downloads the entire MySQL table into a local file in CSV format.
    """
    user, password = get_user_password()  # Assuming these functions are already defined
    database = input("Please enter your MySQL database:\n")
    conn = mysql.connector.connect(
        host='localhost',
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()

    # SQL query to select all rows from the table
    cursor.execute("SELECT * FROM reddit_posts")

    # Fetch all rows
    rows = cursor.fetchall()

    # Specify the column headers for the CSV file
    headers = [i[0] for i in cursor.description]

    # Write to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)  # Write the headers first
        writer.writerows(rows)  # Write the data rows

    print(f"Data successfully written to {filename}")

    # Close database connection
    conn.close()

# Call this function after you've inserted posts into the database
download_table_to_file('reddit_posts.csv')
