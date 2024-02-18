import os
import re

import pandas as pd

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from collections.abc import Iterable # resolving an ImportError
#from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models.doc2vec import TaggedDocument


from get_mysql_data import get_dataset_from_mysql

# functions
'''preprocess function: 
tokenize, remove stopwords, lemmatize, lowercase, remove punctuation
Since Doc2Vec requires input of: (list_of_tokens, tag-id of list_of_tokens)
We use TaggedDocument to add a tag
'''
def preprocess_docs(docs_list, training=True):

	# clean docs list container
	clean_docs_list = []

	# clean each text in docs_list
	for i, text in enumerate(docs_list):

		# remove numbers
		text_nonum = re.sub(r'\d+', '', text)

		# tokenize and remove punctuation
		tokenizer = RegexpTokenizer(r'\w+')
		tokens = tokenizer.tokenize(text_nonum)

		# initialize stopwords list
		sw_list = stopwords.words('english')

		# initialize 
		lemmatizer = WordNetLemmatizer()

		# remove stopwords, lemmatize, and lowercase text
		clean_tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word not in sw_list]

		# snce 
		if training:
			clean_docs_list.append(TaggedDocument(clean_tokens, [i]))

		else:
			clean_docs_list.append(clean_tokens)


	return clean_docs_list

def get_vec_representations(model, data_len):

	len_range = range(int(data_len))

	vec_list = [list(model.dv[i]) for i in len_range]


	return pd.DataFrame(vec_list)

if __name__ == '__main__':

	# results folder path
	res_path = 'results'
	mod_save_path = os.path.join(res_path, 'Doc2Vec.mod')
	vec_save_path = os.path.join(res_path, 'Doc2Vec_vec.csv')

	# set vector representation size
	vector_size = 30

	print('Retrieving Data from MySQL\n')
	df, con = get_dataset_from_mysql()

	content = df.loc[:, 'content']

	print('Cleaning Text')
	# clean and tag documents
	clean_docs = preprocess_docs(content, training = True)

	print('Initializing Model')
	# initialize a Document and train
	# min_count = 3 to remove really infrequent words
	model = Doc2Vec(vector_size = vector_size, min_count=2, epochs = 40)

	# build the vocabulary
	model.build_vocab(clean_docs)

	print('Training Model')
	# train
	model.train(clean_docs, total_examples=model.corpus_count, epochs=model.epochs)

	model.save(mod_save_path)
	print(f'Model saved to {mod_save_path}')

	print('Outputting Text Vector Representations')
	vec_df = get_vec_representations(model, model.corpus_count)

	vec_df.to_csv(vec_save_path)
	print(f'Outputted vector representations to {vec_save_path}')

	con.close()
