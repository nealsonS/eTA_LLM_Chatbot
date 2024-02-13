Lab 4 part 1

### keyword_extraction.py
updated version of data_collection.py that preprocess the data and extracts keyword from content column and adds a keyword column to the table

### berTopic.py
tool to use BERT modelling to topic modelling to assign each headline to a topic
It adds columns: ['Topic' and 'Topic_Keywords'] to the reddit_posts table

### check_missing.py
this checks for missing content values and checks what the corresponding url is. if the url is an article, it will scrape the link for content to use as the reddit post's own content. if the url is a youtube link, audio file link, or an unreachable link, the content will be replaced with a message indicating this finding.



### 'ignore' folder
this contains the files we did not end up using for different reasons. These are 'spacy.py', 'rake.py', and 'data_collection.py' 

### data_collection.py:
collects data from reddit using praw and upload the collected data to mysql

### download_table.py
a tool to download the specific table from mysql to better view the full content of the table (because on phpadmin it does not display full content if it is too long)