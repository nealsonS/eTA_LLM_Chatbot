import praw
import mysql.connector
import re
from datetime import datetime

# Initialize PRAW with your Reddit App credentials
reddit = praw.Reddit(client_id='EBX_xza7Pe9nyTLmXcYGJg',
                     client_secret='UgjKmwJ6G2uPvR2imghS1RiMGxWdXw',
                     user_agent='script:DSCI560:v1 (by /u/your_reddit_username)')

def fetch_posts(subreddit, limit):
    subreddit = reddit.subreddit(subreddit)
    for post in subreddit.hot(limit=limit):
        yield {
            'title': post.title,
            'content': post.selftext,
            'created_at': datetime.fromtimestamp(post.created),
            'url': post.url
        }

def preprocess_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def get_user_password():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'
    password = input("Please enter your MySQL password:\n")
    return user, password

host = 'localhost'
user, password = get_user_password()
database = input("Please enter your MySQL database:\n")

conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cursor = conn.cursor()

# Create table (if not exists)
cursor.execute('''
CREATE TABLE IF NOT EXISTS reddit_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    content TEXT,
    created_at DATETIME,
    url TEXT
)''')
conn.commit()

# Alter table if it already exists and the 'url' column is not TEXT
cursor.execute('''
ALTER TABLE reddit_posts MODIFY COLUMN url TEXT
''')
conn.commit()

def store_posts(subreddit, limit):
    for post in fetch_posts(subreddit, limit):
        post['content'] = preprocess_text(post['content'])
        # Make sure the URL is a string, just in case
        post['url'] = str(post['url'])
        cursor.execute('''
        INSERT INTO reddit_posts (title, content, created_at, url)
        VALUES (%s, %s, %s, %s)''', (post['title'], post['content'], post['created_at'], post['url']))
    conn.commit()

store_posts('tech', 100)  # Modify the limit as per your requirement
