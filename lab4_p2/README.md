Lab 4 part 2

Typical/Recommended workflow:
1. Create a database on mysql server (preferably 'lab4')
2. Run `keyword_extraction.py` to scrape and add reddit_posts table to the database
3. Run `topic_modelling.py` to get topic assignment through bert model
	It adds columns: `Topic`, `Topic_Name`, `Topic_Keywords` to the reddit_posts table
....

Script Brief Overview:
### _.py:
blurb about the code
