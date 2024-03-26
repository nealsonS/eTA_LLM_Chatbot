import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings,  HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import HuggingFaceHub
from langchain.llms.huggingface_pipeline import HuggingFacePipeline

# older import versions
#from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings 
#from langchain.vectorstores import FAISS
#from langchain.chat_models import ChatOpenAI
#from langchain.llms import LlamaCpp
#from langchain import HuggingFacePipeline


# extra packages for our code
#from transformers import GPT2Tokenizer, GPT2LMHeadModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import fitz  # PyMuPDF
import os



# our code to store pdf data into database, instead of skeleton code get_pdf_text() 
def extract_content_from_pdf(pdf_path): 
    doc = fitz.open(pdf_path)
    try:
        text_pages = []
        image_paths = []
        
        for page_number in range(doc.page_count):
            page = doc[page_number]
            text_pages.append(page.get_text("text") + " ")

            # extract images and save to a file
            images = page.get_images(full=True)
            page_image_paths = []  # list to store all image paths for one page
            image_number = 1   

            for img_index, img in enumerate(images):
                image_index = img[0] 
                base_image = doc.extract_image(image_index)
                image_bytes = base_image["image"]

                # save image to png file
                image_path = f'./images/page_{page_number+1}_image_{image_number}.png' 
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_bytes)

                page_image_paths.append(image_path)
                image_number += 1
            
            image_paths.append(page_image_paths)

        return text_pages, image_paths

    finally:
        doc.close()



def get_text_chunks(text_list):
    text_str = "".join(text_list)
    text_splitter = CharacterTextSplitter(
        separator="\n", 
        chunk_size=500, #must be 500
        chunk_overlap=200, #better performance than 100
        length_function=len
    )
    chunks = (text_splitter.split_text(text_str))
    return chunks


# our code to put chunks into vector store instead of skeleton get_vectorstore(text_chunks). 
# also using huggingface instead of openAI
def embed_chunk_to_vectorstore(chunks):
    embedding_model = HuggingFaceEmbeddings()
    #print('Embed Model Initialized')
    #print('Storing embeddings in vector store, please wait.')
    vectorstore = FAISS.from_texts(chunks, embedding_model)
    #print('Stored embeddings in vector store!')
    return vectorstore



class LocalGPT2:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.model.eval()  # Set the model to evaluation mode

    def generate_response(self, prompt_text):
        input_ids = self.tokenizer.encode(prompt_text, return_tensors='pt')
        output_sequences = self.model.generate(
            input_ids,
            #max_length=100,
            max_new_tokens = 50, 
            temperature=0.7, # OG 0.7
            top_p=1.0, # OG 0.9
            do_sample=True,
            num_return_sequences=1, # OG 1
            pad_token_id = 50256
        )
        generated_text = self.tokenizer.decode(output_sequences[0], skip_special_tokens=True)
        return self



def get_conversation_chain(vectorstore):
    #llm = LocalGPT2()

    llm = HuggingFaceHub(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        huggingfacehub_api_token = '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',
        task="text-generation",
        model_kwargs={
            "max_new_tokens": 512,
            "top_k": 40,
            "temperature": 0.8,
            "repetition_penalty": 1.03, 
        },
    )

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    print(llm)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 4}),
        memory=memory,
    )
    return conversation_chain



def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            #print(i, message.content)
        else:
            shrinked_message = ""
            for line in message.content.split("\n"):
                if line.strip().startswith("Helpful Answer:"):
                    shrinked_message = line.strip().replace("Helpful Answer:", "").strip() # we only want the last "helpful answer" 
            st.write(bot_template.replace(
                "{{MSG}}", shrinked_message), unsafe_allow_html=True)
            #print(i, shrinked_message)




def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with PDFs",
                       page_icon=":robot_face:")
    st.write(css, unsafe_allow_html=True)
    
    styl = f""" 
    <style>
        .stTextInput {{
          position: fixed;
          bottom: 3rem;
        }}
    </style>
    """
    st.markdown(styl, unsafe_allow_html=True) #moves text input box down 


    if "conversation" not in st.session_state:
        st.session_state.conversation = None #not meant for users to have no PDF processed
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Gain more insights from your PDFs :mag_right:")
    user_question = st.text_input("Ask anything about your document(s):")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click 'Process'", type=["pdf"], accept_multiple_files=True) 

        temp_file_path = os.path.join(os.getcwd(), "uploaded_files.pdf")
        for doc in pdf_docs:
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(doc.getvalue()) 
                print(temp_file)   
        if st.button("Process"):
            with st.spinner("Processing... Please wait"):
                # get pdf text
                raw_text, raw_pics = extract_content_from_pdf(temp_file) # pdf_docs would work as a path
                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                # create vector store
                vectorstore = embed_chunk_to_vectorstore(text_chunks)
                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)



if __name__ == '__main__':
    main()
