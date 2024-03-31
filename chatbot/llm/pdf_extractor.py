import os
import sys
import shutil
import mysql.connector
from mysql.connector import errorcode
import fitz  # PyMuPDF



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


# extract text content and images from PDF using PyMuPDF
def extract_content_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    try:
        
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

                # save the image to png file
                image_path = f'./images/page_{page_number+1}_image_{image_number}.png' 
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_bytes)

                page_image_paths.append(image_path)
                image_number += 1
            
            image_paths.append(page_image_paths)

        return text_pages, image_paths

    finally:
        doc.close()



def parse_details(doc_name, page, text, image):
    details = {
        "doc_name": "Unknown",
        "page": "Unknown",
        "text_content": "None",
        "image_path": "None",
    }
    details["doc_name"] = doc_name
    details["page"] = str(page+1)
    details["text_content"] = text
    details["image_path"] = image #make sure have all images on page
    return details


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


def create_or_delete_contents_of_folder(path, folder_name):

    # create folder if not exist
    if os.path.exists(path):
        folder_contents = os.listdir(path)

        is_empty = len(folder_contents) == 0

        if not is_empty:
            print(f'{folder_name} folder is not empty!\nProceed Anyways?')
            img_action = input('Type Y to proceed or N to stop execution or R to remove its contents:\n').strip().upper()

            while img_action not in ['Y', 'N', 'R']:
                print('Invalid input!')
                img_action = input('Type Y to proceed or N to stop execution or R to remove its contents:\n').strip().upper()

            if img_action == 'N':
                sys.exit(1)

            if img_action == 'R':
                for file_path in folder_contents:
                    parent, fname = os.path.split(file_path)
                    _, img_folder = os.path.split(parent)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f'Failed to delete {os.path.join(img_folder, fname)} for reason: {e}')

    else:
        os.makedirs(path)

# Combine all scripts
def get_pdf_text():
    #host = 'localhost'
    #user = 'root'
    #password = ''
    #database = 'demo1'
    host, user, password, database = get_mysql()
    connection = connect_to_database(host, user, password, database)
    cursor = connection.cursor()

    #pdf_directory = '/home/vboxuser/0/lab6/drive'
    pdf_directory = input("Please enter the path to the folder that contains the pdf file:\n")
    img_folder_path = os.path.join('.', 'images')
    # create folder if not exist
    # if there are contents in folder, ask what to do with it
    create_or_delete_contents_of_folder(img_folder_path, 'Image')

    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)

            #extract text content and images
            extracted_text, extracted_images = extract_content_from_pdf(pdf_path)
            print(f"Extracted text and image for '{filename}'")

            for e in range(len(extracted_text)):
                details = parse_details(filename, e, extracted_text[e], extracted_images[e])
                insert_data_into_db(cursor, details)

    print(f"Uploaded to '{database}' database")

    # delete img folder after execution
    #shutil.rmtree(img_folder_path)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    get_pdf_text()

