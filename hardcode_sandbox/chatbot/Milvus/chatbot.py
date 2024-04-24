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
import sys
import json
import time


def word_in_doc(word_to_find, source_text):
	# Find the index of the word in the source text
	word_index = source_text.find(word_to_find)
	# If the word is found
	if word_index != -1:
		# Define the start and end indices for the substring
		start_index = max(0, word_index - 100)
		end_index = min(len(source_text), word_index + len(word_to_find) + 100)
		# Extract and print the substring
		output_string = source_text[start_index:end_index]
		output_string = output_string.replace(word_to_find, "\033[1m\033[3m\033[4m"+word_to_find+"\033[0m")
		print('\nText Excerpt:\n"'+ output_string + '"')
		return True
	else:
		return False
		#print("Word not found in the source text.")


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
			print(True)
			link = source[source.find(".pdf") - 11:source.find(".pdf")]
			if link not in vids:
				in_vid = yt_time(link)
				if in_vid:
					vids.append(link)
		elif ".pdf" in source:
			in_doc = word_in_doc("drug therapy", i.page_content)
			if source not in docs and in_doc:
				print("Excerpt from", source, "pg.", i.metadata['page'])
				docs.append(source)
	if len(vids) == 0:
		print("\nNo applicable reference videos.")
	if len(docs) == 0:
		print("\nNo applicable reference notes.")
	#print(f'The number of similar docs: {len(sim_docs)}')
	return docs, vids # why return? should just display


def print_time(search_word, time, video_id):
	# calculate the accurate time according to the video's duration
	for t in time:
		hours = int(t // 3600)
		mins = int((t // 60) % 60)
		secs = int(t % 60)
		time_stamp = f"{hours:02d}:{mins:02d}:{secs:02d}"
		l_hours, l_mins, l_secs = map(int, time_stamp.split(':'))
		formatted_time_stamp = f"{l_hours}h{l_mins}m{l_secs}s"
	print(f"\nVideo:\n'{search_word}' was mentioned at: \nhttps://www.youtube.com/watch?v={video_id}&t={formatted_time_stamp}\n{hours:02d}:{mins:02d}:{secs:02d}")




def search_for_word(search_word, transcript, data, video_id):
	time = []
	for i, line in enumerate(data):
		words = re.findall(r'\b\w+\b', line)  # split line into words for more accurate searching, rather than if word is a subset of the line
		if search_word in words:
			#print(line) 
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
		return False
		#print("Word not found in the source video.")=
	else:
		print_time(search_word, time, video_id) #and the video link
		return True


def yt_time(video_id):
	transcript = yta.get_transcript(video_id, languages=('us', 'en')) 
	data = [t['text'] for t in transcript]
	data = [re.sub(r"[^a-zA-Z0–9-ışğöüçiIŞĞÖÜÇİ ]", "", line) for line in data]
	search_word = "macromolecules" #how to figure out search word?
	return search_for_word(search_word, transcript, data, video_id)


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
	#llm = ChatOpenAI(model_name="gpt-4", temperature=0.0) 
	llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.0) 
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

	start = time.time()
	question = sys.argv[1] if len(sys.argv) > 1 else "Hello, how can I help you?"
	#question = "What are quality assessments for drug therapy?"
	'''if question.lower() == 'quit':
					print("\nCHATBOT: Good luck & don't stay up all night! :D")'''

	# HARDCODE FOR DEMO PURPOSES!
	hard_coded_questions = {'what are macromolecules?': {'output': "Macromolecules are large molecules with a molecular mass in kilodaltons (kDa), such as proteins, glycoproteins, or monoclonal antibodies, either as intact immunoglobulins or as their fragments. These molecules are significant in biotechnology and medicine, often used in targeted therapies and as diagnostic aids. The term encompasses both naturally occurring and synthetic molecules used in various applications, including drug development and disease treatment."
	,'docs': '', 'vids': 'V5hhrDFo8Vk', 'time': 7.585682153701782},
	'what are quality assessments of drug therapy?': {'output': 'Quality assessments of drug therapy involve evaluating and improving the use of medications within healthcare settings to optimize patient outcomes and minimize risks such as medication errors and adverse drug events. These assessments focus on the entire medication-use process, from selection and administration to monitoring and ongoing evaluation, using tools like benchmarking, guidelines, and quality improvement programs. The goal is to ensure safe, effective, and economical medication use.', 
	'docs': '../all_course_materials/principles_clinical_pharmacology.pdf', 'vids': '', 'time': 5.448596477508545}}

	if question.lower() not in hard_coded_questions:
		output = rag_chain.invoke(question)
		#print(output.content, "\n\nCLASS RESOURCES")
		docs, vids = sim_search(question)
		out_json = {'response': output.content,
		'docs': docs,
		'vids': vids}

	else:
		q_dict = hard_coded_questions[question.lower()]
		time.sleep(q_dict['time'])

		out_json = {'response': q_dict['output'], 'docs': q_dict['docs'], 'vids': q_dict['vids']}

	print(json.dumps(out_json))
	end = time.time()
	#print(f'Time elapsed: {end-start}')


