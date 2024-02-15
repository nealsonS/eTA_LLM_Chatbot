from get_mysql_data import get_dataset_from_mysql
# for nltk_clustering()
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
# for scikit_clustering()
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


# uncomment if you need to download theses
#nltk.download('stopwords')
#nltk.download('punkt')
	
	
	
	
def nltk_clustering(documents):
	# preprocess post content
	stop_words = set(stopwords.words('english'))
	tokenized_documents = [word_tokenize(doc.lower()) for doc in documents]
	filtered_documents = [[word for word in doc if word.isalnum() and word not in stop_words] for doc in tokenized_documents]
	preprocessed_documents = [' '.join(doc) for doc in filtered_documents]

	# convert text data into TF-IDF vectors
	vectorizer = TfidfVectorizer()
	X = vectorizer.fit_transform(preprocessed_documents)

	# k-means clustering
	num_clusters = 10  # Adjust the number of clusters as needed
	kmeans = KMeans(n_clusters=num_clusters, random_state=42)
	clusters = kmeans.fit_predict(X)

	# display clustering results
	for i, doc in enumerate(documents):
	    print(f"Document #{i + 1} - Cluster #{clusters[i]}")
	    #print(f"Document #{i + 1} - Cluster #{clusters[i]}: {doc}")
	
	# Reduce dimensionality for visualization
	svd = TruncatedSVD(n_components=2)
	X_reduced = svd.fit_transform(X)

	# Create a scatter plot for visualizing clusters
	plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=clusters, cmap='viridis')
	plt.title('Document Clustering Visualization')
	plt.xlabel('Principal Component 1')
	plt.ylabel('Principal Component 2')
	plt.show()





def scikit_clustering(documents):
	# convert text data into bag-of-words representation
	# countvectorizer seem to be the weaker of the 2
	vectorizer = CountVectorizer(max_features=1000, stop_words='english')
	X = vectorizer.fit_transform(documents)
	# fit a latent dirichlet allocation (LDA) model
	num_topics = 3  # Adjust the number of topics as needed
	lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
	lda.fit(X)

	# display top words for each topic
	feature_names = vectorizer.get_feature_names_out()
	for topic_idx, topic in enumerate(lda.components_):
	    top_words_idx = topic.argsort()[:-10 - 1:-1]
	    top_words = [feature_names[i] for i in top_words_idx]
	    print(f"Topic #{topic_idx + 1}: {', '.join(top_words)}")




if __name__ == '__main__':
	print('Retrieving Data from MySQL\n')
	df, con = get_dataset_from_mysql()
	content = df.loc[:, 'content']
	print(len(content))

	documents = content
	
	# nltk_clustering(documents)
	scikit_clustering(documents)


