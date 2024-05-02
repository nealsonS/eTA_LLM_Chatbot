## argument_rag_res.py
Script that answers user queries using RAG, HuggingFace embeddings, and GPT-4 as LLM. <br>
Precursor to `../chatbot.py`.
1. Inputs user query when running script (example: `python3 argument_rag_res.py "what are macromolecules?"`)
2. Outputs response to query 
3. Also ouputs relevant PDFs and YouTube video links / timestamps


## chatbot_working.py
Script that answers user queries using RAG, HuggingFace embeddings, and GPT-4 as LLM. <br>
Tries to implement timer to keep track of how long it took the program to run.
1. Inputs user query
2. Outputs response to query 
3. Also ouputs relevant PDFs and YouTube video links / timestamps
4. Also ouputs time elapsed


## feedback_rag_res.py
Script that answers user queries using RAG, HuggingFace embeddings, and GPT-4 as LLM. <br>
Tries to implement feedback insertion into Milvus database.
1. Inputs user query
2. Outputs response to query until user inputs 'quit'
3. Also ouputs relevant PDFs and YouTube video links / timestamps


## keywords.py
Script that answers user queries using RAG, HuggingFace embeddings, and GPT-4 as LLM. <br>
Tries to implement keyword search to help with document / video retrieval parallel to similarity search.
1. Inputs user query
2. Outputs response to query until user inputs 'quit'
3. Also ouputs relevant PDFs and YouTube video links / timestamps


## rag_res.py
Script that answers user queries using RAG, HuggingFace embeddings, and GPT-4 as LLM. <br>
Precursor to `../chatbot.py`.
1. Inputs user query
2. Outputs response to query until user inputs 'quit'


## mem_rag_res.py
Script that answers user queries using RAG, HuggingFace embeddings, and GPT-4 as LLM. <br>
Tries to implement conversation memory with Conversation Buffer Window Memory.
1. Inputs user query
2. Outputs response to query until user inputs 'quit'
3. Also ouputs conversation history of chat


## convo_memory.py
Script that tests different conversation memory modules for optimal results.
1. Tests Conversation Buffer Memory
2. Tests Conversation Summary Memory
3. Tests Conversation Summary Buffer Memory
4. Tests Conversation Buffer Window Memory


## rag_chain.py 
Basic implementation of RAG chatbot to check if vector database works.
1. Inputs user query
2. Outputs response to query based on HuggingFace embeddings.


## sim_search.py
Script that performs similarity search of user-inputted query to HuggingFace embeddings stored in Milvus. 
1. Inputs user query
2. Pulls the most similar texts in the collection


## milvus_sandbox.py
Quick script to test connection with Milvus database.


## quick_drop_collections.py (USE FOR TESTING ONLY)
DANGEROUS: This script is the same as `../Milvus/drop_collections.py` but doesn't ask the user to make sure. <br>
Made this to quickly drop collections quickly for testing insertions. 
