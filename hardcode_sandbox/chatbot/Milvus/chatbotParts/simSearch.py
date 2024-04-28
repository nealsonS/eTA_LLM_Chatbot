from chatbotParts.keywordExtractor import find_keywords
from chatbotParts.ytVideo import yt_time 
from chatbotParts.pdfExcerpt import word_in_doc

from langchain.vectorstores.milvus import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings


def sim_search(query, embeddings, connection_args, COLLECTION_NAME):
	vectorstore = Milvus(
		embedding_function = embeddings,
		connection_args=connection_args,
		collection_name = COLLECTION_NAME
	)
	sim_docs = vectorstore.similarity_search(query)
	docs = []
	doc_pages = []
	vids = []
	vid_times = []
	keywords = find_keywords(query)
	for i in sim_docs:
		#print(i.metadata['source']) #format works
		#print(i.metadata['pk'])
		source = i.metadata['source'].replace("/home/vboxuser/chatbot", "..") #might need to replace this??
		if "ytvid_" in source:
			link = source[source.find(".pdf") - 11:source.find(".pdf")]
			if link not in vids:
				for word in keywords:
					in_vid, timestamp = yt_time(link, word)
					if in_vid:
						vid_times.append(timestamp)
						vids.append(link)
		elif ".pdf" in source:
			for word in keywords:
				in_doc, output_string, page_number = word_in_doc(word, i.page_content, source)
				if source not in docs and in_doc:
					#print(output_string)
					#print("For {word},\nExcerpt from", source, "pg.", i.metadata['pk'])
					docs.append(source)
					doc_pages.append(page_number)
	#if len(vids) == 0:
	#	print("\nNo applicable reference videos.")
	#if len(docs) == 0:
	#	print("\nNo applicable reference notes.")
		
	return docs, doc_pages, vids, vid_times
