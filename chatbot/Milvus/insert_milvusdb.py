from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.milvus import Milvus
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from pymilvus import utility
from pymilvus import connections, db

import os
import time 

def insert_pdfs_chunks(pdf_list, embedding_model, COLLECTION_NAME):
	connection_args = { 'uri': URI }
	text_splitter = CharacterTextSplitter(
		chunk_size=1000,
		chunk_overlap=200,
	)
	num_pdfs = len(pdf_list)

	for f in pdf_list:
		start = time.time() # for checking time

		loader = PyPDFLoader(f)
		pages = loader.load_and_split()
		docs = text_splitter.split_documents(pages)

		vectorstore = Milvus(
				embedding_function=embedding_model,
				connection_args=connection_args,
				collection_name=COLLECTION_NAME,
				drop_old=False,
			).from_documents(
				docs,
				embedding=embedding_model,
				collection_name=COLLECTION_NAME,
				connection_args=connection_args,
			)

		num_pdfs -= 1
		print(f'Inserted! {f}')
		print(f'Duration: {time.time() - start}, PDFS left: {num_pdfs}\n')

def insert_text_chunks(text_list, delim, embedding_model, COLLECTION_NAME):
	connection_args = { 'uri': URI }
	text_splitter = CharacterTextSplitter(
	separator=delim, 
	chunk_size=1000,
	chunk_overlap=200, #better performance than 100
	length_function=len
	)

	num_texts = len(text_list)

	for f in text_list:
		start = time.time()
		loader = TextLoader(f)
		text_str = loader.load_and_split()

		chunks = (text_splitter.split_documents(text_str))

		vectorstore = Milvus(
			embedding_function=embedding_model,
			connection_args=connection_args,
			collection_name=COLLECTION_NAME,
			drop_old=False,
		).from_documents(
			chunks,
			embedding=embedding_model,
			collection_name=COLLECTION_NAME,
			connection_args=connection_args,
			)

		num_texts -= 1
		print(f'Inserted! {f}')
		print(f'Duration: {time.time() - start}, texts left: {num_texts}\n')


def handle_user_input():
	FOLDER_PATH = input('Please input the folder path where texts/pdfs are located:\n')

	while not os.path.exists(FOLDER_PATH):
		print('ERROR! Folder path inputted is invalid!')

		FOLDER_PATH = input('Please input file path of the text file to be inserted:\n')

	return FOLDER_PATH

def get_file_paths(FOLDER_PATH):

	texts, pdfs, others = set(), set(), set()

	for f in os.listdir(FOLDER_PATH):

		fname, ext = f.split('.')

		if ext.lower() == 'pdf':
			pdfs.add(os.path.join(FOLDER_PATH, f))
		elif ext.lower() == 'txt':
			texts.add(os.path.join(FOLDER_PATH, f))
		else:
			others.add(os.path.join(FOLDER_PATH, fname))

	return texts, pdfs, others

if __name__ == '__main__':

	COLLECTION_NAME = 'db_560'
	host = 'localhost'
	port = '19530'
	URI = f'http://{host}:{port}' # connection address for milvus

	connections.connect(
		alias = 'default',
		host = host,
		port= port
		)

	delim = '\n'

	FOLDER_PATH = handle_user_input()

	texts, pdfs, others = get_file_paths(FOLDER_PATH)

	embedding_model = HuggingFaceEmbeddings()


	COLLECTION_EXISTS = utility.has_collection(COLLECTION_NAME)
	if not COLLECTION_EXISTS: # check if collection already exists

		insert_text_chunks(texts, delim, embedding_model, COLLECTION_NAME)
		insert_pdfs_chunks(pdfs, embedding_model, COLLECTION_NAME)
	else:
		print(f'{COLLECTION_NAME} already exists!\nExiting...')


