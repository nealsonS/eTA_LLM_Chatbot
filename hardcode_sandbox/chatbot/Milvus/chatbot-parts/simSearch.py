from keywordExtractor import find_keywords
from ytVideo import yt_time 
from pdfExcerpt import word_in_doc

from langchain.vectorstores.milvus import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
#from langchain.chains import ConversationChain
#from langchain.chains.conversation.memory import ConversationBufferMemory
#from langchain.callbacks import get_openai_callback
#from langchain_community.callbacks import get_openai_callback
#from langchain.chains.conversation.memory import ConversationSummaryMemory
#from langchain.chains.conversation.memory import ConversationBufferWindowMemory
#from langchain.chains.conversation.memory import ConversationSummaryBufferMemory



def sim_search(query):
	#message = find_keywords(), yt_time(), word_in_doc(), "sim_search imported"
	#return message
	docs = ['doc1']
	vids = ['vid1']
	return docs, vids 




def sim_search_real(query):
	vectorstore = Milvus(
		embedding_function = embeddings,
		connection_args=connection_args,
		collection_name = COLLECTION_NAME
	)
	sim_docs = vectorstore.similarity_search(query)
	docs = []
	vids = []
	keywords = find_keywords(query)
	for i in sim_docs:
		#print(i.metadata['source']) #format works
		#print(i.metadata['page'])
		source = i.metadata['source'].replace("/home/vboxuser/chatbot/all_course_materials/", "") #might need to replace this??
		if "ytvid_" in source:
			link = source[source.find(".pdf") - 11:source.find(".pdf")]
			if link not in vids:
				for word in keywords:
					in_vid = yt_time(link, word)
					if in_vid:
						vids.append(link)
		elif ".pdf" in source:
			for word in keywords:
				in_doc = word_in_doc(word, i.page_content)
				if source not in docs and in_doc:
					print("For {word},\nExcerpt from", source, "pg.", i.metadata['page'])
					docs.append(source)
	if len(vids) == 0:
		print("\nNo applicable reference videos.")
	if len(docs) == 0:
		print("\nNo applicable reference notes.")
	#print(f'The number of similar docs: {len(sim_docs)}')
	return docs, vids # why return? should just display
