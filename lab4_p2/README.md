Lab 4 part 2

Typical/Recommended workflow:
Part 1:
1. Create a database on mysql server (preferably 'lab4')
2. Run `keyword_extraction_p1.py` to scrape and add reddit_posts table to the database
3. Run `topic_modelling_p1.py` to get topic assignment through bert model
	It adds columns: `Topic`, `Topic_Name`, `Topic_Keywords` to the reddit_posts table

Part 2:
1. For the full automation code, run `automation.py`
2. For only vector representations of documents, run `text_abstraction_Doc2Vec_demo.py` 
	saved in results/Doc2Vec_vec.csv
3. For only the clustering of articles based on topics, run `optnumtop_demo.py`
	saved in results/tech_clusters.html.


Script Brief Overview:
### automation.py
	Run this script for the full program performance on `Content`
	column of reddit_posts table from MySQL
	
	Input:
	1. It asks user to input interval values and keywords / messages to find the topic of
	2. It retrieves data from MySQL
	Output: 
	1. inputted user keywords' topic and list of reddit posts in that same topic
	2. tech_clusters.html - visualization of clusters
	3. results/Doc2Vec.mod - Trained Gensim Doc2Vec model (can be loaded)
	4. results/Doc2Vec_vec.csv - Vector representations of all the documents


### text_abstraction_Doc2Vec.py
	Run this script to get vector representations of `Content`
	column of reddit_posts table from MySQL

	Input: 
	1. It retrieves data from MySQL
	Output: 
	1. results/Doc2Vec.mod - Trained Gensim Doc2Vec model (can be loaded)
	2. results/Doc2Vec_vec.csv - Vector representations of all the documents
	
	Note:
	The _demo.py allows you to run this alone.
	
	
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

	Note:
	The _demo.py allows you to run this alone.

	
	
Helper scripts overview:
### get_mysql_data.py
	Import the function `get_dataset_from_mysql()` from this script
	which retrieves reddit_posts table from MySQL server
	Output:
	1. df- Dataframe
	2. conn- connection to the MySQL database

### keyword_extraction_p1.py
	Import the function `store_posts()` from this scripts 
	which runs the keyword extraction program to scrape, preprocess, 
	and do keyword extraction on reddit posts.

### topic_modelling_p1.py
	Import the function `topic_modeling()` from this scripts 
	which runs the bertopic modeling program get topic assignment 
	for the "title" of the reddit posts, not the "content".














