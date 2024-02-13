from bertopic import BERTopic
import pandas as pd
import numpy as np
import mysql.connector
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
from sklearn.feature_extraction.text import CountVectorizer

# get data
def get_user_password():
    user = input("Please enter your MySQL user:\nLeave Blank if it is root\n")
    user = user or 'root'
    password = input("Please enter your MySQL password:\n")
    return user, password

host = 'localhost'
user, password = get_user_password()
#database = input("Please enter your MySQL database:\n")
database = input("Please enter your MySQL database:\n")
print('Connecting to Database!\n')
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cursor = conn.cursor()

query = f"SELECT title FROM reddit_posts"
cursor.execute(query)

rows = cursor.fetchall()

columns = [col[0] for col in cursor.description]

df = pd.DataFrame(rows, columns=columns)

# PREPROCESSING!

# get the title
docs = df['title'].to_numpy()

# Modelling!

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

print('Modelling Topic!\n')

topics, probs = topic_model.fit_transform(docs)

# get topic count and keywords to csv
topic_info_df = pd.DataFrame(topic_model.get_topic_info())
topic_info_df.to_csv('topics_info.csv')

# get each topic and their appropriate topics
topics_label = topic_model._map_predictions(topic_model.hdbscan_model.labels_)

#probs = hdbscan.all_points_membership_vectors(topic_model.hdbscan_model)
#probs = topic_model._map_probabilities(probs, original_topics=True)

# save to original docs
df.loc[:, 'topic'] = topics_label
df.loc[:, 'topic_keywords'] = ''

for i in topic_info_df.index:
	i_str = ', '.join(topic_info_df.loc[i, 'Representation'])
	df.loc[df.loc[:, 'topic'] == i, 'topic_keywords'] = i_str

# add column topic and topic_keywords to SQL table
col_add_query = """ALTER TABLE reddit_posts
ADD COLUMN IF NOT EXISTS Topic INT,
ADD COLUMN IF NOT EXISTS Topic_Keywords VarChar(255);"""
cursor.execute(col_add_query)
# set column to 0
cursor.execute('UPDATE reddit_posts SET Topic = NULL;')
cursor.execute('UPDATE reddit_posts SET Topic_Keywords = NULL;')

def insert_to_table(cursor, tb_name, f_df):
	
	# convert to None to avoid loading in NumPy
	f_df = f_df.fillna(np.nan).replace([np.nan], [None])
	
	# list of values
	val_arr = f_df.values.tolist()

	query=f"""INSERT INTO {tb_name} 
	(Topic, Topic_Keywords) VALUES
	({', '.join(['%s' for i in f_df.columns])});
	"""
	
	cursor.executemany(query, val_arr)

# insert data to columns
out_df = df.loc[:, ['topic', 'topic_keywords']]

insert_to_table(cursor, 'reddit_posts', out_df)
con.close()