from piazza_api import Piazza
from html2text import HTML2Text
import os
import re

HTML_2_TEXT = HTML2Text()
HTML_2_TEXT.ignore_links = True

EMAIL = None
PASSWORD = None


def main():
    piazza = Piazza()
    piazza.user_login()
    #piazza.user_login(email=EMAIL, password=PASSWORD)
    network_id = 'lr7e73kounllq' #piazza ID for DSCI 560
    #network_id = input("Input your course's Piazza network ID: ").strip()
    course = piazza.network(network_id)
    posts = course.iter_all_posts(limit=10)
    filename = input("Name of the file to write Piazza posts to (don't add '.txt'): ").strip()
    filename = filename + ".txt"
    with open(filename, 'w') as f:
        for post in posts:
            post_content = post['history'][0]['content']
            post_content_as_text = HTML_2_TEXT.handle(post_content)
            post_content_as_text = post_content_as_text.replace('\n', ' ')
            post_content_as_text = post_content_as_text.replace('  ', ' ')
            post_content_as_text = post_content_as_text.strip()
            post_content_as_text = re.sub(r'!\[\]\(.*\)', '', post_content_as_text)
            f.write(post_content_as_text + '\n')

if __name__ == '__main__':
    main()

