from pymilvus import MilvusClient

# 1. Set up a Milvus client
client = MilvusClient(
    uri="http://35.215.73.196:19530"
)

COLLECTION_NAME = 'db_560'
