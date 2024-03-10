import os
import mysql.connector
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class LocalGPT2:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.model.eval()  # set model to evaluation mode

    def generate_response(self, prompt_text):
        input_ids = self.tokenizer.encode(prompt_text, return_tensors='pt')
        output_sequences = self.model.generate(
            input_ids,
            #max_length=100,
            max_new_tokens = 50, 
            temperature=0.7, # best temp
            top_p=1.0, # best value for output
            do_sample=True,
            num_return_sequences=1, # best value 
            pad_token_id = 50256
        )
        generated_text = self.tokenizer.decode(output_sequences[0], skip_special_tokens=True)
        return generated_text[len(prompt_text):]



def connect_to_database(host, user, password, database):
    try:
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT text_content FROM cookbook")
            rows = cursor.fetchall()
            return [row[0] for row in rows]  
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()



def get_text_chunks(text_content):
    print(text_content)
    all_chunks = []
    for t in text_content:
        text = str(t)
        text_splitter = CharacterTextSplitter(
            separator="\n", 
            chunk_size=500, #must be 500
            chunk_overlap=200, # changed from 100, 200 seems to perform a bit better
            length_function=len
        )
        chunks = (text_splitter.split_text(text))
        all_chunks.extend(chunks)  
    return all_chunks

def embed_chunk_to_vectorstore(chunks):
    embedding_model = HuggingFaceEmbeddings()
    print('Embed Model Initialized')
    print('Storing embeddings in vector store, please wait.')
    vectorstore = FAISS.from_texts(chunks, embedding_model)
    print('Stored embeddings in vector store!')
    return vectorstore

def main():
    host = 'localhost'
    user = 'root'
    password = ''
    database = 'demo1'
    
    # get raw text from the database
    raw_text = connect_to_database(host, user, password, database)
    # prcess raw text into chunks
    text_chunks = get_text_chunks(raw_text)
    # embed chunks into vector store (simplified for this example)
    vectorstore = embed_chunk_to_vectorstore(text_chunks)
    
    # initialize GPT-2 model
    llm = LocalGPT2()
    # simulate conversation
    print("Let's chat! Type 'exit' to end the conversation.")
    while True:
        user_input = input(">>> You: ")
        if user_input.lower() == 'exit':
            break
        # simplified use of vectorstore in conversation
        # actual use would involve querying the vectorstore based on the user input
        num_chunks_for_context = 1 # best value for performance
        context_list = [x.page_content for x in vectorstore.similarity_search(user_input)[:num_chunks_for_context]]
        context_str = " \n".join(context_list)
        prompt =  f"""Context: \n{context_str}
Question: {user_input}
Answer: 
        """ # using first 3 chunks as context for simplicity
        response = llm.generate_response(prompt)
        print(">>> AI:", response)

if __name__ == '__main__':
    main()
