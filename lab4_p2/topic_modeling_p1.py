from bertopic import BERTopic
import pandas as pd
import numpy as np
import mysql.connector
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
from sklearn.feature_extraction.text import CountVectorizer
from get_mysql_data import get_dataset_from_mysql 

# Modelling!

def init_model():
	# initialize embedding model
	embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

	# to perform dimension reduction
	umap_model = umap.UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)

	# to control number of topics
	hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=5, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

	# to remove stopwords and ignore infrequent words
	vectorizer_model = CountVectorizer(stop_words="english", min_df=2, ngram_range=(1, 2))

	# create pipeline
	topic_model = BERTopic(

	  embedding_model=embedding_model,
	  umap_model=umap_model,
	  hdbscan_model=hdbscan_model,
	  vectorizer_model=vectorizer_model
		)

	return topic_model

def insert_to_mySQL(df, con):

	cursor = con.cursor()
	def check_column_existence(table_name, column_name, cursor):
		query = f"SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '{table_name}' AND column_name = '{column_name}'"
		cursor.execute(query)
		return cursor.fetchone()[0]

	def insert_to_table(cursor, tb_name, f_df):
		
		# convert to None to avoid loading in NumPy
		f_df = f_df.fillna(np.nan).replace([np.nan], [None])
		f_df.loc[:, 'id'] = f_df.index.values + 1
		
		# list of values
		val_arr = f_df.values.tolist()

		insert_query = f"""INSERT INTO {tb_name} (Topic, Topic_Name, Topic_Keywords, id) VALUES (%s, %s, %s, %s) 
		ON DUPLICATE KEY UPDATE Topic=VALUES(Topic), Topic_Name=VALUES(Topic_Name), Topic_Keywords=VALUES(Topic_Keywords)"""

		# if Topic and Topic_Keywords not in reddit_posts table, add it
		for col in ['Topic', 'Topic_Name', 'Topic_Keywords']:

			col_dtype ={'Topic': 'INT', 'Topic_Name': 'VARCHAR(255)', 'Topic_Keywords': 'VARCHAR(255)'}

			if not check_column_existence('reddit_posts', col, cursor):

				# add column topic and topic_keywords to SQL table
				col_add_query = f"""ALTER TABLE reddit_posts
				ADD COLUMN {col} {col_dtype[col]};"""
				cursor.execute(col_add_query)
				con.commit()

		cursor.executemany(insert_query, val_arr)
		con.commit()

	# insert data to columns
	insert_to_table(cursor, 'reddit_posts', df)

def topic_modeling():

	df, con = get_dataset_from_mysql()
	cursor = con.cursor()

	# get the title of each row and convert to numpy
	docs = df['title'].to_numpy()

	# initialize the model
	topic_model = init_model()

	# fit the model to get topics and probabilities
	topics, probs = topic_model.fit_transform(docs)

	# get topic info to a dataframe
	topic_info_df = pd.DataFrame(topic_model.get_topic_info())
	topic_info_df.to_csv('topics_info.csv')

	# get topic assignment
	topics_label = topic_model._map_predictions(topic_model.hdbscan_model.labels_)

	#probs = hdbscan.all_points_membership_vectors(topic_model.hdbscan_model)
	#probs = topic_model._map_probabilities(probs, original_topics=True)

	# save to original docs
	df.loc[:, 'topic'] = topics_label
	df.loc[:, 'topic_name'] = ''
	df.loc[:, 'topic_keywords'] = ''

	for i in topic_info_df.index:
		df.loc[df.loc[:, 'topic'] == i, 'topic_name'] = topic_info_df.loc[i, 'Name']

		r_str = '/'.join(topic_info_df.loc[i, 'Representation'])
		df.loc[df.loc[:, 'topic'] == i, 'topic_keywords'] = r_str

	out_df = df.loc[:, ['topic', 'topic_name', 'topic_keywords']]

	insert_to_mySQL(out_df, con)
	con.commit()
	con.close()
