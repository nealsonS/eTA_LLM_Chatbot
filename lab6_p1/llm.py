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
        self.model.eval()  # Set the model to evaluation mode

    def generate_response(self, prompt_text):
        input_ids = self.tokenizer.encode(prompt_text, return_tensors='pt')
        output_sequences = self.model.generate(
            input_ids,
            max_length=150,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            num_return_sequences=1,
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
            return [row[0] for row in rows]  # Adjusted to return a list of text_content directly
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def get_text_chunks(text_contents):
    all_chunks = []
    text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=500, chunk_overlap=100, length_function=len)
    for text in text_contents:
        chunks = text_splitter.split_text(text)
        all_chunks.extend(chunks)
    return all_chunks

def embed_chunk_to_vectorstore(chunks):
    embedding_model = HuggingFaceEmbeddings()

    vectorstore = FAISS.from_texts(chunks, embedding_model)
    return vectorstore

def main():
    host = 'localhost'
    user = 'root'
    password = 'password'
    database = 'lab6'
    
    # Fetch raw text from the database
    raw_text = connect_to_database(host, user, password, database)
    
    # Process the text into chunks
    text_chunks = get_text_chunks(raw_text)
    
    # Embed these chunks into a vector store (simplified for this example)
    vectorstore = embed_chunk_to_vectorstore(text_chunks)
    
    # Initialize the GPT-2 model
    llm = LocalGPT2()
    
    # Simulate conversation
    print("Let's chat! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        # Simplified use of vectorstore in conversation
        # Actual use would involve querying the vectorstore based on the user input
        prompt = " ".join(vectorstore[:3]) + "\n" + user_input  # Using first 3 chunks as context for simplicity
        response = llm.generate_response(prompt)
        print("AI:", response)

if __name__ == '__main__':
    main()
