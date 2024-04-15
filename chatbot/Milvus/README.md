# Vector Database with Milvus
Milvus is an open-source high-performance popular vector database solution. <br>
It benchmarks quite fast, so it'd be perfect to use for our chatbot to speed up searches for context. <br>
Since we have a large PDF collection and text files, it would be unfeasible to reload everything into the vector database everytime. <br>
So, I proposed having a milvus server running on your machine and adding everything into it. Then after this, the chatbot connects to it via localhost:19530 (the default port and ip for localhost milvus) <br>

## Requirements
Please run on terminal on Ubuntu:
```
wget https://github.com/milvus-io/milvus/releases/download/v2.3.12/milvus_2.3.12-1_amd64.deb
sudo apt-get update
sudo dpkg -i milvus_2.3.12-1_amd64.deb
sudo apt-get -f install
```
and:
```
pip3 install grpcio-tools
pip3 install protobuf==3.20.0
pip install pymilvus==2.3.4
pip install milvus-cli==0.4.2
pip install langchain
pip install sentence_transformers
pip install pypdf
```

## Files
### insert_milvus_db.py
This script asks for the folder path which contains text and pdf files. <br>
Then for each pdf and text file, it embeds using HuggingFaceEmbedding model and adds it to a collection named: `db_560` <br>
To avoid duplication of data, it will fail if the collection already exists <br>

### sim_search.py
Quick implementation to perform similarity search of user-inputted query. <br>
It will pull the most similar texts in the collection. <br>

### drop_collections.py
This scripts connects to your Milvus server, and list all the collections inside your server. <br>
Then it asks you to type `YES_DELETE_ALL` to delete all the collections or `exit` to exit. <br>
This is to avoid accidental deletion of collection.

### quick_drop_collections.py (USE FOR TESTING ONLY)
DANGEROUS: This scripts is the same as drop_collections.py but doesn't user to make sure. <br>
Made this to quickly drop collections quickly for testing insertions. <br>

### rag_chain.py (TESTING, WIP)
Quick basic implementation of RAG chatbot to check if vector database works. <br>
Will be adjusting parameters. <br>

## Extra information
Use the milvus_cli (command line interface) to see collections:
```
# to run the cli
milvus_cli

# to see any collections
list collections

# to see details of collections
show collection -c COLLECTION_NAME

exit
```


If you want to check status of your milvus server, run:
```
sudo systemctl status milvus
sudo systemctl status milvus-etcd
sudo systemctl status milvus-minio
```



