from pathlib import Path
import time
from streamlit_chat import message
import streamlit as st
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import UnstructuredExcelLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import tempfile
import pandas as pd
import matplotlib.pyplot as plt
import os


# -------------------We will Load the file using this function-----------------------
def load_data(filename):
    if 'csv' in filename:
        loader = CSVLoader(file_path = filename, encoding = 'utf8', csv_args = {'delimiter': ','})
        data = loader.load()
        return data
    if 'xlsx' in filename:
        loader = UnstructuredExcelLoader(file_path = filename, encoding = 'utf8', mode="elements")
        data = loader.load()
        return data

def memory_store():
    # Memory model configuration
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages= True
    )
    
    memory.save_context({"input": "Hi"}, 
                    {"output": "What's up"})
    return memory

# ------------------- Building the model --------------------
def chat(query,data_path):
    
    data = load_data(data_path)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})
    vectordb = FAISS.from_documents(documents = data, embedding = embeddings)
    vectordb.save_local('vectorstore/db_faiss')
    # LLM Model configuration
    llm = CTransformers(
        model = "llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        max_new_tokens = 512,
        temperature = 0.5
    )
    
    # Chaining model configuration
    chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever=vectordb.as_retriever(),
        memory = memory_store(),
        verbose = True
    )
    
    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    
    return result['answer']

st.set_page_config(page_title="Atleos ChatBot", page_icon="Images/ai-icon.jpg")
uploaded_files = st.sidebar.file_uploader("Upload File", type=["csv","xlsx"])

if uploaded_files :

    save_path = "Data/"+uploaded_files.name
    with open(save_path, mode='wb') as w:
        w.write(uploaded_files.getvalue())

    if os.path.exists(save_path):
        alert = st.success(f'File {uploaded_files.name} is successfully saved!')
        time.sleep(2)
        alert.empty()
    # Application configuration

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello ! Ask me anything about"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey ! 👋"]


    st.markdown("<h1 style='text-align: center; color: white;'>Chat Bot</h1>", unsafe_allow_html=True)
    response_container = st.container()
    container = st.container()
    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Query:", placeholder="Talk to your csv data here: ", key='input')
            submit_button = st.form_submit_button(label='Send')
                    
        if submit_button and user_input:
            output = chat(user_input,save_path)
                    
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="adventurer")
                message(st.session_state["generated"][i], key=str(i), avatar_style="bottts")
else:
    st.markdown("<h2 style='text-align: center; color: white;'>Upload the csv/xlsx Data to start the Conversation with AI🤖</h2>", unsafe_allow_html=True)