import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_BASE_URI = os.getenv("MONGODB_BASE_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")

# OpenAI Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)

# Initialize MongoDB python client with Atlas connection URI
MONGODB_ATLAS_CLUSTER_URI = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_BASE_URI}/{MONGODB_DATABASE}?retryWrites=true&w=majority"
client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

DB_NAME = MONGODB_DATABASE
COLLECTION_NAME = "embeddings"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

vector_store = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding=embeddings,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)

# Load and Process PDFs
folder_path = "../all_course_materials"
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=["\n\n", "\n", "(?<=\. )", " "], length_function=len)

for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        loader = PyMuPDFLoader(pdf_path)
        documents = loader.load()

        # Split the loaded documents into chunks
        split_docs = splitter.split_documents(documents)
        print('Split into ' + str(len(split_docs)) + ' docs')

        # Store the documents in the MongoDB vector store
        vector_store.add_documents(split_docs)
        print(f"Processed and stored {filename} in MongoDB.")
