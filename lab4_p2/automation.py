from get_mysql_data import get_dataset_from_mysql 
from topic_modeling_p1 import topic_modeling 
from keyword_extraction_p1 import store_posts
from text_abstraction_Doc2Vec import text_abstraction
from optnumtop import optnumtop
import mysql.connector
import time
import threading

# get data
def get_user_password_db():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'
    password = input("Please enter your MySQL password:\n")
    database = input("Please enter your MySQL database:\n")
    return user, password, database

def get_connection(user, password, database):

    host = 'localhost'
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    return conn

# scraping, preprocessing, and storage updated every X minutes
def background_task(conn):
    print('Scraping, preprocessing, and storing data')
    df, conn = store_posts('tech', 100, conn)
    topic_modeling(df, conn)
        

if __name__ == '__main__':
    while True:
        interval_input = input("Input intervals in minutes that the database will be updated, separated by space. Type 'quit' at the end. (EX: '5 10 quit' for 5 minutes then 10 minutes)\n")
        # Check if 'quit' is not present in the input
        if 'quit' not in interval_input.lower():
            print("Invalid input. 'quit' must be present. Please try again.")
            continue
        break
    interval_list = [inp for inp in interval_input.split()]
    intervals = []
    for inp in interval_list:
    	if inp.isdigit():
    	    seconds = int(inp) * 60
    	    intervals.append(seconds)
    #print(intervals)

    # find rolling difference
    if len(intervals) > 1:
        diff_i = [j-i for i, j in zip(intervals[:-1], intervals[1:])]
    else:
        diff_i = []

    user, password, db = get_user_password_db()
    conn = get_connection(user, password, db)
    background_task(conn)

    if len(diff_i) > 0:
        for i in diff_i:
            print(f'Waiting {i} seconds')
            time.sleep(i)
            conn = get_connection(user, password, db)

            # background thread for tasks
            #background_thread = threading.Thread(target=background_task, args=(df, conn, i))
            #background_thread.start()
            background_task(conn)


   # continue with other main thread tasks
   # while not updating, take keyword, then it should be clustered again and output the cluster topic and a graphical representation.
    keywords = input("Enter keywords to find the best cluster they could belong in, separated by space\n")
    #keywords_list = [k for k in keywords.split()]
    optnumtop(df, keywords)
    text_abstraction(df)
    # wait for background threads to complete (optional)
    #background_thread.join()

    conn.commit()
    conn.close
 
