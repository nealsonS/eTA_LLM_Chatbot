Lab 4 part 2

Typical/Recommended workflow:
Part 1:
1. Create a database on mysql server (preferably 'lab4')
2. Run `keyword_extraction.py` to scrape and add reddit_posts table to the database
3. Run `topic_modelling.py` to get topic assignment through bert model
	It adds columns: `Topic`, `Topic_Name`, `Topic_Keywords` to the reddit_posts table

Part 2:
1. Run `text_abstraction_Doc2Vec.py` to get vector representations of documents
	saved in results/Doc2Vec_vec.csv
2.

Script Brief Overview:
### text_abstraction_Doc2Vec.py
	Run this script to get vector representations of `Content`
	column of reddit_posts table from MySQL

	Input: 
	1. It retrieves data from MySQL
	Output: 
	1. results/Doc2Vec.mod- Trained Gensim Doc2Vec model (can be loaded)
	2. results/Doc2Vec_vec.csv - Vector representations of all the documents
	
	
### optnumtop.py 
	Run this script to get topic clustering of `Content`
	column of reddit_posts table from MySQL

	Input: 
	1. It retrieves data from MySQL
	Output: 
	1. finds the optimal number of topics from documents
	2. uses LDA to do topic modeling for the optimal number of topics
	3. displays a 70-character snippet of the documents under each topic
	4. creates HTML file in folder to open and view visualization
	
	
	
### clustering.py (IGNORE FOR NOW)
	Run this script to get topic clustering of `Content`
	column of reddit_posts table from MySQL

	Input: 
	1. It retrieves data from MySQL
	Output: 
	1. for nltk_clustering(), you will get a list of the documents (reddit posts) and their estimated clusters out of n clusters. A scatterplot will also appear to show the clusters.
	2. for scikit_clustering(), you will get a list of n topics with the top 10 keywords for each topic
	
	
### gensim_clustering.py  (IGNORE FOR NOW, code reused for optnumtop.py)
	Run this script to get topic clustering of `Content`
	column of reddit_posts table from MySQL

	Input: 
	1. It retrieves data from MySQL
	Output: 
	1. uses LDA to do topic modeling
	2. creates HTML file in folder to open and view visualization
	
	
Helper scripts overview:
### get_mysql_data.py
	Import the function `get_dataset_from_mysql()` from this script
	which retrieves reddit_posts table from MySQL server
	Output:
	1. df- Dataframe
	2. conn- connection to the MySQL database
