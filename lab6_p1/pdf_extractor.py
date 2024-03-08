import os
import sys
import mysql.connector
from mysql.connector import errorcode
import fitz  # PyMuPDF

global_figure_counter = -0
# Get MySQL username, password, database
def get_mysql():
    host = 'localhost'
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'  # Defaults to 'root' if left blank
    password = input("Please enter your MySQL password:\n")
    database = input("Please enter your MySQL database:\n")
    return host, user, password, database

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

# Extract text content and images from PDF using PyMuPDF
def extract_content_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text_pages = []
        image_paths = []

        for page_number in range(doc.page_count):
            page = doc[page_number]
            text_pages.append(page.get_text("text") + " ")

            # Extract images and save to a file
            images = page.get_images(full=True)
            page_image_paths = []  # list to store all image paths for one page
            image_number = 1   
            for img_index, img in enumerate(images):
                image_index = img[0] 
                base_image = doc.extract_image(image_index)
                image_bytes = base_image["image"]
                
                # Save the image to a file
                image_path = f'./images/page_{page_number+1}_image_{image_number}.png' 
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_bytes)

                page_image_paths.append(image_path)
                image_number += 1
            
            image_paths.append(page_image_paths)

        return text_pages, image_paths

    finally:
        doc.close()

# have text column and image column?
def parse_details(page, text, image):
    details = {
        "page": "Unknown",
        "text_content": "None",
        "image_path": "None",
    }
    details["page"] = str(page+1)
    details["text_content"] = text
    details["image_path"] = image #make sure have all images on page
    #print(details["page"])
    return details

# Create MySQL table in database
def check_and_create_table(cursor):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cookbook (
        id INT AUTO_INCREMENT PRIMARY KEY,
        page VARCHAR(255),
        text_content TEXT,
        image_path VARCHAR(255)
    )
    """
    cursor.execute(create_table_sql)

# Insert data into database
def insert_data_into_db(cursor, details):
    check_and_create_table(cursor)  # Ensure table exists
    for image_path in details["image_path"]:
        insert_sql = """
        INSERT INTO cookbook (page, text_content, image_path) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_sql, (details["page"], details["text_content"], image_path))

# Combine all scripts
def main():
    #host = 'localhost'
    #user = 'root'
    #password = ''
    #database = 'demo1'
    host, user, password, database = get_mysql()
    connection = connect_to_database(host, user, password, database)
    cursor = connection.cursor()

    #pdf_directory = '/home/vboxuser/0/lab6/drive'
    pdf_directory = input("Please enter the path to the  pdf file:\n")
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)

            # Extract text content and images
            extracted_text, extracted_images = extract_content_from_pdf(pdf_path)
            print(f"Extracted text and image for '{filename}'")

            for e in range(len(extracted_text)):
                details = parse_details(e, extracted_text[e], extracted_images[e])
                insert_data_into_db(cursor, details)

    print(f"Uploaded to '{database}' database")

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    main()

