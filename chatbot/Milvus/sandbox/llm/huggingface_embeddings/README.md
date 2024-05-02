# Testing performance and integration of various HuggingFace embeddings 

## all_conn_emb.py
Script to connect to HuggingFace database to retrieve all course materials embeddings and answer queries.
1. Connects to HuggingFace database and retrieves course materials embeddings
2. Outputs answer to inputted question
3. Optionally, can output the similarity score of embeddings to question


## all_to_emb.py
Script that transforms all PDF documents in `../all_course_materials` into embeddings. 
1. Transforms PDF files into embeddings
2. Outputs embeddings into single CSV file (sample output file in folder)


## tb_conn_emb.py
Script to connect to HuggingFace database to retrieve textbook embeddings and answer queries. <br>
Precursor to `all_conn_emb.py`.
1. Connects to HuggingFace database and retrieves textbook embeddings
2. Outputs answer to inputted question
3. Optionally, can output the similarity score of embeddings to question


## tb_to_emb.py
Script that transforms `textbook.pdf` into embeddings. <br>
Precursor to `all_to_emb.py`.
1. Transforms textbook into embeddings
2. Outputs embeddings into CSV file (sample output file in folder)


## starter_conn_emb.py
Starter code to connect to HuggingFace database to retrieve embeddings and answer queries.
1. Connects to HuggingFace database and retrieves embeddings
2. Outputs answer to inputted question


## starter_to_emb.py
Starter code to test HuggingFace model `all-MiniLM-L6-v2`.
1. Transforms inputted text into embeddings
2. Outputs embeddings into CSV file (sample output file in folder)
