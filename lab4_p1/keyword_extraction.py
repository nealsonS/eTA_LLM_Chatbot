import praw
import mysql.connector
import re
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure you have NLTK resources downloaded
nltk.download('punkt')
nltk.download('stopwords')

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

# NLTK keyword extraction 
# def extract_keywords(text):
#     """
#     Extracts keywords from text using NLTK for tokenization and stopword removal.
#     """
#     stop_words = set(stopwords.words('english'))
#     word_tokens = word_tokenize(text)
#     keywords = [word for word in word_tokens if word not in stop_words and word.isalpha()]
#     return ', '.join(keywords)

# Default Rake
# def extract_keywords(text):
#     # Initialize RAKE by providing a list of stopwords
#     rake = RAKE.Rake(RAKE.SmartStopList())
    
#     # Extract keywords. The run method returns a list of tuples (keyword, score)
#     keywords = rake.run(text)
    
#     # For simplicity, let's return only keywords, not scores, and join them into a string
#     keywords = ', '.join([keyword for keyword, score in keywords])
#     return keywords

# From rake.py
def extract_keywords(text):
    r = Rake()  # Initialize RAKE
    r.extract_keywords_from_text(text)
    keyword_phrases = r.get_ranked_phrases()  # Extract keyword phrases ranked by relevance
    keywords = ', '.join(keyword_phrases)  # Join phrases into a single string
    return keywords



def get_user_password():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'
    password = input("Please enter your MySQL password:\n")
    return user, password

def store_posts(subreddit, limit):
    """
    Stores fetched and processed posts into a MySQL database.
    """
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

    # Create table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reddit_posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title TEXT,
        content TEXT,
        created_at DATETIME,
        url TEXT,
        keywords TEXT
    )''')

    for post in fetch_posts(subreddit, limit):
        processed_content = preprocess_text(post['content'])
        keywords = extract_keywords(processed_content)
        
        cursor.execute('''
        INSERT INTO reddit_posts (title, content, created_at, url, keywords)
        VALUES (%s, %s, %s, %s, %s)''', 
        (post['title'], processed_content, post['created_at'], post['url'], keywords))
        
    conn.commit()
    conn.close()

store_posts('tech', 100)
