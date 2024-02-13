Lab 4 part 1

### data_collection.py:
collects data from reddit using praw and upload the collected data to mysql

### keyword_extraction.py
updated version of data_collection.py that preprocess the data and extracts keyword from content column and adds a keyword column to the table

### download_table.py
a tool to download the specific table from mysql to better view the full content of the table (because on phpadmin it does not display full content if it is too long)

### berTopic.py
tool to use BERT modelling to topic modelling to assign each headline to a topic
It adds columns: ['Topic' and 'Topic_Keywords'] to the reddit_posts table
