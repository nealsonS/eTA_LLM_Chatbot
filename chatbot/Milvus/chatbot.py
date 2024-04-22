import sys
from langchain.vectorstores.milvus import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains import ConversationChain

# Initialize your resources
embeddings = HuggingFaceEmbeddings()
llm = ChatOpenAI(model_name="gpt-4", temperature=0.0)  # Adjust model as needed

# Setup Milvus and other configurations
COLLECTION_NAME = 'db_560'
host = 'localhost'
port = '19530'
URI = f'http://{host}:{port}'
connection_args = {'uri': URI}

retriever = Milvus(
    embedding_function=embeddings,
    connection_args=connection_args,
    collection_name=COLLECTION_NAME
).as_retriever()

# Define the prompt template
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.
{context}
Question: {question}
Helpful Answer:"""

rag_prompt = PromptTemplate.from_template(template)

# Setup the conversational chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
)

def get_response(user_input):
    """
    This function takes user input and returns the AI response.
    """
    try:
        output = rag_chain.invoke(user_input)
        return output.content  # Return only the content of the response
    except Exception as e:
        return str(e)  # Return error message if something goes wrong

if __name__ == '__main__':
    # Take the first argument from command line as input
    user_input = sys.argv[1] if len(sys.argv) > 1 else "Hello, how can I help you?"
    response = get_response(user_input)
    print(response)
