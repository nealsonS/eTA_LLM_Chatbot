from langchain.vectorstores.milvus import Milvus
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
import os



def ai_answer(question, embeddings, connection_args, COLLECTION_NAME):
	
	retriever = Milvus(
		embedding_function = embeddings,
		connection_args = connection_args,
		collection_name = COLLECTION_NAME
	).as_retriever()

	#llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0) 
	os.environ['OPENAI_API_KEY'] = 'sk-proj-CPHp04nMoMj4vJ3EvYFVT3BlbkFJpnFyy8xjVtcx9tGwpdvc'
	llm = ChatOpenAI(model_name="gpt-4", temperature=0.95) 
	# temp = 0.95 is good, for now 0.0 for testing

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
	output = rag_chain.invoke(question)
	return output.content

