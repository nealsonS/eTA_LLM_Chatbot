import praw
import mysql.connector
import re
from datetime import datetime
from rake_nltk import Rake
import requests
from bs4 import BeautifulSoup
from newspaper import Article


# Initialize PRAW with your Reddit App credentials
reddit = praw.Reddit(client_id='EBX_xza7Pe9nyTLmXcYGJg',
                     client_secret='UgjKmwJ6G2uPvR2imghS1RiMGxWdXw',
                     user_agent='script:DSCI560:v1 (by /u/your_reddit_username)')

def fetch_posts(subreddit, limit=100):
    """
    Fetches posts from a given subreddit.
    """
    subreddit = reddit.subreddit(subreddit)
    for post in subreddit.hot(limit=limit):
        yield {
            'title': post.title,
            'content': post.selftext,
            'created_at': datetime.fromtimestamp(post.created),
            'url': post.url
        }

def preprocess_text(text):
    """
    Preprocesses the text by removing HTML tags and special characters.
    """
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    return text


# From rake.py
def extract_keywords(text, num_keywords=10):
    r = Rake()  # Initialize RAKE
    r.extract_keywords_from_text(text)
    keyword_phrases = r.get_ranked_phrases()  # Extract keyword phrases ranked by relevance
    limited_keywords = keyword_phrases[:num_keywords]
    keywords = ', '.join(limited_keywords)  # Join phrases into a single string
    return keywords



# Modified article_scraper function to use Newspaper3k
def article_scraper(link):
    print("Collecting reddit post data, please wait.")
    #print(f"Attempting to scrape content from: {link}")
    article = Article(link)
    try:
        article.download()
        #print("Download successful, parsing article...")
        article.parse()
        #print("Article parsed successfully.")
        if article.text:
            print("Post content parsed successfully.")
            #print(f"Extracted content length: {len(article.text)} characters")
        else:
            print("No content extracted.")
        return article.text
    except Exception as e:
        error_message = f"Failed to download or parse article: {e}"
        print(error_message)
        return error_message


def check_url(urls):
	url_content = [] # will need to add this to mysql !!!!!!!!!!!!!!!!!!!!!!!!!
	for u in urls:
		if "youtu.be" in u or "youtube.com" in u:
		#	print("YouTube video link")
			url_content.append("YouTube video link")
		elif "soundcloud" in u or "open.spotify" in u:
		#	print("Audio link")
			url_content.append("Audio link")
		elif "reddit.com" in u:
		#	print("Reddit link")
			url_content.append("Reddit link")
		else:
		#	print("***Possibly article link!!!")
			url_content.append(article_scraper(u))
	return url_content


def get_user_password():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'
    password = input("Please enter your MySQL password:\n")
    return user, password
    
    
# create database if not exist
def create_database(db_name, user, password):

    # connect to database
    # THIS ASSUMES USER IS ROOT
    try:
        con = mysql.connector.connect(
            user=user, 
            password=password,
            host='127.0.0.1')
            
    # if connection has problem (Error Handling):
    # from: https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            
        # stop the program
        sys.exit("Connection Error! Stopping program...")

    # get cursor to execute queries on database
    cursor = con.cursor()

    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_name.lower()}')

    # close the connection
    con.close()



def store_posts(subreddit, limit):

    """
    Stores fetched and processed posts into a MySQL database.
    """
    host = 'localhost'
    user, password = get_user_password()
    database = input("Please enter your MySQL database:\n")

    # create database if not exists
    create_database(database, user, password)
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()
    # create table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reddit_posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title TEXT,
        content MEDIUMTEXT,
        created_at DATETIME,
        url TEXT,
        keywords MEDIUMTEXT
    )''')
    for post in fetch_posts(subreddit, limit):
        processed_content = preprocess_text(post['content']) if post['content'] else None
        # Check if content is empty
        if not processed_content or processed_content.strip() == '':
            # Attempt to scrape content or identify the type of link
            scraped_content_or_type = check_url([post['url']])
            processed_content = scraped_content_or_type[0] if scraped_content_or_type else "Content could not be retrieved"
        
        keywords = extract_keywords(processed_content)
        
        cursor.execute('''
        INSERT INTO reddit_posts (title, content, created_at, url, keywords)
        VALUES (%s, %s, %s, %s, %s)''', 
        (post['title'], processed_content, post['created_at'], post['url'], keywords))
    conn.commit()
    conn.close()

#store_posts('tech', 100)
