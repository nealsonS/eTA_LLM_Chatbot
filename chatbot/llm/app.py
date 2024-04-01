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


# new imports!
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings


# extra packages for our code
#from transformers import GPT2Tokenizer, GPT2LMHeadModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import fitz  # PyMuPDF
import os




def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=730, #700 better than 600 / 500, not sure if 730 better than 700
        chunk_overlap=350, #since chunk size is 700, try to increase. 350 + 730 good, 700 + 200 good
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    #embeddings = HuggingFaceEmbeddings()
    #embeddings = HuggingFaceEmbeddings(
    #    model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    #llm = HuggingFaceHub(
    #    repo_id="HuggingFaceH4/zephyr-7b-beta",
    #    huggingfacehub_api_token = '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',
    #    task="text-generation",
    #    model_kwargs={
    #        "max_new_tokens": 512,
    #        "top_k": 40,
    #        "temperature": 0.8,
    #        "repetition_penalty": 1.03, 
    #    },
    #)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
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
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        #else: # this version of 'else' is for huggingface vectorstore
        #    shrinked_message = ""
        #    for line in message.content.split("\n"):
        #        if line.strip().startswith("Helpful Answer:"):
        #            shrinked_message = line.strip().replace("Helpful Answer:", "").strip() # we only want the last "helpful answer" 
        #    st.write(bot_template.replace(
        #        "{{MSG}}", shrinked_message), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with PDFs",
                       page_icon=":robot_face:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with PDFs :robot_face:")
    user_question = st.text_input("Ask questions about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()
