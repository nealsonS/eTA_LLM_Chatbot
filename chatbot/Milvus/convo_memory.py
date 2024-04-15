from langchain.vectorstores.milvus import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
#from langchain_openai import OpenAIEmbedding
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory


openai_api_key = "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"


# testing from https://www.pinecone.io/learn/series/langchain/langchain-conversational-memory/
def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        print(f'>>> Spent a total of {cb.total_tokens} tokens')
    return result #answer to query


# won't use this
def con_buf(llm, queries): 
	conversation_history = ConversationChain(
		llm=llm,
		memory=ConversationBufferMemory()
	)
	for q in queries:
		print(count_tokens(conversation_history, q))
	print("\n---CONVO HISTORY---")
	print(conversation_history.memory.buffer)

# won't use this
def con_sum(llm, queries):
	conversation_history = ConversationChain(
		llm=llm,
		memory=ConversationSummaryMemory(llm=llm)
	)
	for q in queries:
		print(count_tokens(conversation_history, q))
	print("\n---CONVO HISTORY---")
	print(conversation_history.memory.prompt.template)
	print("\n---CONVO SUMMARY---")
	print(conversation_history.memory.buffer)


# won't use this
def con_sum_bufw(llm, queries):
	conversation_history = ConversationChain(
	llm=llm, memory=ConversationSummaryBufferMemory(
		llm=llm,
		max_token_limit=650)
	)
	for q in queries:
		print(count_tokens(conversation_history, q))
	#not sure if this will work here...
	bufw_history = conversation_history.memory.load_memory_variables(inputs=[])['history']
	print("\n---CONVO HISTORY---")
	print(bufw_history)


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


# from lab 6
def get_conversation_chain(llm):#, question):
	conversation_history = ConversationChain(llm=llm)
	#llm = ChatOpenAI()
	#memory = ConversationBufferMemory(
		#memory_key='chat_history', return_messages=True)
		#conversation_chain = ConversationalRetrievalChain.from_llm(
		#llm=llm,
		#retriever=vectorstore.as_retriever(
		#search_type="similarity", search_kwargs={"k": 4}),
		#memory=memory,
	#)
	#print(conversation_history.prompt.template)

	#return conversation_history(question)


if __name__ == '__main__':

	COLLECTION_NAME = 'db_560'
	host = 'localhost'
	port = '19530'
	URI = f'http://{host}:{port}' # connection address for milvus
	connection_args = { 'uri': URI }

	embeddings = HuggingFaceEmbeddings()
	#embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
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
	
	questions=[
	"What are quality assessments for drug therapy?",
	"Select the one lettered answer or statement completion that is BEST. It may be helpful to carry out dimensional analysis by including units in your calculations. Answers are provided in Appendix II. A 35-year-old woman is being treated with gentamicin for a urinary tract infection. The gentamicin plasma level is 4 mg/mL shortly after initial intravenous administration of an 80-mg dose of this drug. What is the answer to this question?",
	"What are macromolecules?",
	"What is the answer to the previous question?",
	"What is my previous question?"
]

	while True:
		question = input("YOU: ")
		#question = "What are quality assessments for drug therapy?"
		if question.lower() == 'quit':
			print("\nCHATBOT: Good luck!")
			break
		output = rag_chain.invoke(question)
		print("\nCHATBOT:", output.content, "\n")
		print("----- MEMORY -----")
		#print(get_conversation_chain(llm, question))
		con_bufw(llm, question)

	
	# testing memory
	#get_conversation_chain(llm)
	#con_buf(llm, questions)
	#con_sum(llm, questions)
	#con_sum_bufw(llm, questions)






