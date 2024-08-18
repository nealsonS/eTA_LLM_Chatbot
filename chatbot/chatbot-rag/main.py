from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain.chains import create_retrieval_chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from pymongo import MongoClient
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# FastAPI application setup
app = FastAPI()

# Get environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_BASE_URI = os.getenv("MONGODB_BASE_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")

# Initialize OpenAI embedding and chat models
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)

# MongoDB connection setup
MONGODB_ATLAS_CLUSTER_URI = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_BASE_URI}/{MONGODB_DATABASE}?retryWrites=true&w=majority"
client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

# MongoDB collection and vector store setup
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

# 1. Create the retriever from the vector store
retriever = vector_store.as_retriever()

# 2. Incorporate the retriever into a question-answering chain.
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

# Create a ChatPromptTemplate using the system prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Create the question-answering chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)

# Create the retrieval-augmented generation (RAG) chain
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Define the input model for FastAPI using Pydantic
class QueryModel(BaseModel):
    query: str

@app.post("/query/")
async def get_answer(query: QueryModel):
    try:
        # Use the `invoke` method to execute the chain with the provided input
        result = rag_chain.invoke({"input": query.query})

        # Extract the answer from the response
        answer = result["answer"]

        # Extract the source document information
        source_documents = result["context"]

        # Compile source details into a list of dictionaries
        sources = [
            {
                "document": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "Unknown")
            }
            for doc in source_documents
        ]

        # Return the combined answer and source details as a JSON object
        response = {
            "answer": answer,
            "sources": sources
        }

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example endpoint to check if the service is running
@app.get("/")
async def root():
    return {"message": "RAG API is running"}

