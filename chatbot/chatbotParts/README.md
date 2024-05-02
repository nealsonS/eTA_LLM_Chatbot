## dbMilvus.py
Script that connects with Milvus database. <br>
Embeddings stored can be created using HuggingFace embeddings, OpenAI embeddings, or VoyageAI embeddings.


## keywordExtractor.py
Script that extracts keywords from user query and returns said keywords.


## pdfExcerpt.py
Script that searches for keywords in PDFs of `../all_course_materials`. <br>
If relevant documents are found, return the string and page number of said string.


## ragChain.py
Script that connects to Milvus database and uses RAG to answer user-inputted queries.


## simSearch.py
Script that connects to Milvus database and does a similarity search of the query to database embeddings. <br>
If relevant documents and videos are found, return these sources.


## ytVideo.py
Script that searches for keywords in YouTube video transcripts of `../all_course_materials`. <br>
If relevant videos are found, return the video link and timestamp of said string.
