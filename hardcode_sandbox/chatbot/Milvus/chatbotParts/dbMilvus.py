from langchain.vectorstores.milvus import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings


def embed():
	COLLECTION_NAME = 'db_560'
	host = 'localhost'
	port = '19530'
	URI = f'http://{host}:{port}' # connection address for milvus
	connection_args = { 'uri': URI }

	embeddings = HuggingFaceEmbeddings()
	#embeddings = OpenAIEmbeddings() # is different shape from HFE, which breaks Milvus
	
	return embeddings, connection_args, COLLECTION_NAME
