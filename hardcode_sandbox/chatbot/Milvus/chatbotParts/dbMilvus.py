from langchain.vectorstores.milvus import Milvus
from langchain_voyageai import VoyageAIEmbeddings
#from langchain_community.embeddings import HuggingFaceEmbeddings



def embed():
	COLLECTION_NAME = 'db_560'
	host = '35.215.73.196'
	port = '19530'
	URI = f'http://{host}:{port}' # connection address for milvus
	connection_args = { 'uri': URI }

	#embeddings = HuggingFaceEmbeddings()
	#embeddings = OpenAIEmbeddings() # is different shape from HFE, which breaks Milvus
	embeddings = VoyageAIEmbeddings(
		voyage_api_key = "pa-cLlD2gK4qGD_AtnXz5A6vqLXjUDIrC4yACyxehLgXd4",
		model = 'voyage-lite-02-instruct'
	)
	
	return embeddings, connection_args, COLLECTION_NAME
