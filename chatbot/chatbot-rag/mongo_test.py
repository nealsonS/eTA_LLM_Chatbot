from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
# uri = "mongodb+srv://ColinZWang:770sGrandAve7058@colinzwang-cluster.6civtdf.mongodb.net/?retryWrites=true&w=majority&appName=ColinZWang-cluster"
# Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection


from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get environment variables
MONGODB_BASE_URI = os.getenv("MONGODB_BASE_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")


# Initialize MongoDB python client with Atlas connection URI
MONGODB_ATLAS_CLUSTER_URI = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_BASE_URI}/{MONGODB_DATABASE}?retryWrites=true&w=majority"
client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)