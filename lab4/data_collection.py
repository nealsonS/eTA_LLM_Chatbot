import praw
import mysql.connector
import re
from datetime import datetime


# Initialize PRAW with your Reddit App credentials
reddit = praw.Reddit(client_id='EBX_xza7Pe9nyTLmXcYGJg',  # Your actual client_id
                     client_secret='UgjKmwJ6G2uPvR2imghS1RiMGxWdXw',  # Your actual client_secret
                     user_agent='script:DSCI560:v1 (by /u/your_reddit_username)')  # Your actual user_agent


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
    # collect password and database of mysql server
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user.lower().strip()
    if user == '':
        user = 'root'
    password = input("Please enter your MySQL password:\n")
    return user, password

host = 'localhost'
user, password = get_user_password()
database = input("Please enter your MySQL database:\n")#'lab3' #change if needed


conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = conn.cursor()

# Create table (if not exists)
cursor.execute('''CREATE TABLE IF NOT EXISTS reddit_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    content TEXT,
    created_at DATETIME,
    url VARCHAR(255)
)''')
conn.commit()

# Fetch and store posts
def store_posts(subreddit, limit):
    for post in fetch_posts(subreddit, limit):
        post['content'] = preprocess_text(post['content'])
        cursor.execute('''INSERT INTO reddit_posts (title, content, created_at, url)
                          VALUES (%s, %s, %s, %s)''',
                       (post['title'], post['content'], post['created_at'], post['url']))
    conn.commit()

# Example usage
store_posts('tech', 100)  # Modify the limit as per your requirement
