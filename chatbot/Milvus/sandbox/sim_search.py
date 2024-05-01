from langchain.vectorstores.milvus import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings

if __name__ == '__main__':

	COLLECTION_NAME = 'db_560'
	host = 'localhost'
	port = '19530'
	URI = f'http://{host}:{port}' # connection address for milvus
	connection_args = { 'uri': URI }

	embeddings = HuggingFaceEmbeddings()
	vectorstore = Milvus(
		embedding_function = embeddings,
		connection_args=connection_args,
		collection_name = COLLECTION_NAME
	)

	input_str = 'Write a search query:\nInput: '
	user_input = input(input_str)

	while user_input.lower() != 'exit':

		sim_docs = vectorstore.similarity_search(user_input)

		for i in sim_docs:
			print(i)
			print()

		print(f'The number of similar docs: {len(sim_docs)}')

		user_input = input(input_str)


