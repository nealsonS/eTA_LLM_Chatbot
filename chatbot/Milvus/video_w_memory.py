from langchain.vectorstores.milvus import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
#from langchain.callbacks import get_openai_callback
from langchain_community.callbacks import get_openai_callback
from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from youtube_transcript_api import YouTubeTranscriptApi as yta
import re


def word_in_doc(word_to_find, source_text):
	# Find the index of the word in the source text
	word_index = source_text.find(word_to_find)
	# If the word is found
	if word_index != -1:
		# Define the start and end indices for the substring
		start_index = max(0, word_index - 50)
		end_index = min(len(source_text), word_index + len(word_to_find) + 50)
		# Extract and print the substring
		output_string = source_text[start_index:end_index]
		print(output_string)
	else:
		print("Word not found in the source text.")


def sim_search(query):
	vectorstore = Milvus(
		embedding_function = embeddings,
		connection_args=connection_args,
		collection_name = COLLECTION_NAME
	)
	sim_docs = vectorstore.similarity_search(query)
	docs = []
	vids = []
	for i in sim_docs:
		#print(i.metadata['source']) #format works
		#print(i.metadata['page'])
		source = i.metadata['source'].replace("/home/vboxuser/chatbot/all_course_materials/", "")
		if "ytvid_" in source:
			link = source[source.find(".pdf") - 11:source.find(".pdf")]
			print(link)
			if link not in vids:
				vids.append(link)
		elif ".pdf" in source:
			print(source, i.metadata['page'])
			word_in_doc("macromolecules", i.page_content)
			if source not in docs:
				docs.append(source)
	print(f'The number of similar docs: {len(sim_docs)}')
	return docs, vids


def print_time(search_word, time, video_id):
    print(f"'{search_word}' was mentioned at: https://www.youtube.com/watch?v={video_id}")
    # calculate the accurate time according to the video's duration
    for t in time:
        hours = int(t // 3600)
        min = int((t // 60) % 60)
        sec = int(t % 60)
        print(f"{hours:02d}:{min:02d}:{sec:02d}")


def search_for_word(search_word, transcript, data, video_id):
	time = []
	for i, line in enumerate(data):
		words = re.findall(r'\b\w+\b', line)  # split line into words for more accurate searching, rather than if word is a subset of the line
		if search_word in words:
			print(line)
			start_time = transcript[i]['start']
			# to accomodate for start time not being the actual word
		text = re.sub(r"(?<=:)([A-Z]+)", "", line).split(' ') # remove stuff like: 'AUDIENCE: '
		try:
			i_word = text.index(search_word) + 1
		except ValueError:
			continue  
		added_time = (i_word / len(text)) * transcript[i]['duration']
		#print(added_time) 
		final_time = start_time + added_time
		time.append(final_time)
	if len(time) == 0:
		print("Word not found.")
	else:
		print_time(search_word, time, video_id)


def yt_time(video_id):
	transcript = yta.get_transcript(video_id, languages=('us', 'en')) 
	data = [t['text'] for t in transcript]
	data = [re.sub(r"[^a-zA-Z0–9-ışğöüçiIŞĞÖÜÇİ ]", "", line) for line in data]
	search_word = "macromolecules" #how to figure out search word?
	search_for_word(search_word, transcript, data, video_id)


# testing from https://www.pinecone.io/learn/series/langchain/langchain-conversational-memory/
def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.invoke(query)
        print(f'>>> Spent a total of {cb.total_tokens} tokens')
    return result #answer to query


def con_bufw(llm, queries):
	conversation_history = ConversationChain(
		llm=llm,
		memory=ConversationBufferWindowMemory(k=2) #change to 10 later
	)
	for q in queries:
		print(count_tokens(conversation_history, q))
	print("\n---CONVO HISTORY---")
	bufw_history = conversation_history.memory.load_memory_variables(inputs=[])['history']
	print(bufw_history)




if __name__ == '__main__':

	COLLECTION_NAME = 'db_560'
	host = 'localhost'
	port = '19530'
	URI = f'http://{host}:{port}' # connection address for milvus
	connection_args = { 'uri': URI }

	embeddings = HuggingFaceEmbeddings()
	#embeddings = OpenAIEmbeddings() # is different shape from HFE, which breaks Milvus
	retriever = Milvus(
		embedding_function = embeddings,
		connection_args=connection_args,
		collection_name = COLLECTION_NAME
	).as_retriever()

	#llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0) 
	llm = ChatOpenAI(model_name="gpt-4", temperature=0.0) 
	# temp = 0.95 is good, for now 0.0 for testing

	# code from https://milvus.io/docs/integrate_with_langchain.md
	template = """Use the following pieces of context to answer the question at the end. 
	If you don't know the answer, just say that you don't know, don't try to make up an answer. 
	Use three sentences maximum and keep the answer as concise as possible. 
	{context}
	Question: {question}
	Helpful Answer:"""

	rag_prompt = PromptTemplate.from_template(template)

	rag_chain = (
 	   {"context": retriever, "question": RunnablePassthrough()}
	    | rag_prompt
	    | llm
	)

	while True:
		question = input("YOU: ")
		#question = "What are quality assessments for drug therapy?"
		if question.lower() == 'quit':
			print("\nCHATBOT: Good luck!")
			break
		docs, vids = sim_search(question)
		for v in vids:
			yt_time(v)
		#output = rag_chain.invoke(question)
		#print("\nCHATBOT:", output.content, "\n")
		#print("----- MEMORY -----")
		#con_bufw(llm, question)







