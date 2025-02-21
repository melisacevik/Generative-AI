from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_google = os.getenv("google_apikey")

llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-pro", convert_system_message_to_human=True)

embeddings = OpenAIEmbeddings(api_key=my_key_openai)

def split_content(splitter_type, target_url="", chunk_size=500, chunk_overlap=0):

    loader = WebBaseLoader(target_url)

    raw_documents = loader.load()

    if splitter_type == "Character":
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

    elif splitter_type == "Recursive":
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

    elif splitter_type == "Semantic":
        text_splitter = SemanticChunker(embeddings)

    splitted_documents = text_splitter.split_documents(raw_documents)

    return splitted_documents

import streamlit as st

st.set_page_config(page_title="Splitter Karşılaştırması", layout="wide")
st.title("Splitter Karşılaştırması")
st.divider()

target_url = st.text_input(label="İşlenecek Web Adresini Giriniz:")
st.divider()
chunk_size = st.slider(label="Kesit büyüklüğünü belirleyiniz:",min_value=100, max_value=2000, value=1000, step=100, key="url_chunk_size")
st.divider()
chunk_overlap = st.slider(label="Çakışma büyüklüğünü belirleyiniz:",min_value=0, max_value=1000, value=0, step=100, key="url_chunk_overlap")
st.divider()
submit_btn = st.button(label="Başla", key="url_button")
st.divider()

if submit_btn:

    col_character, col_recursive, col_semantic = st.columns(3)

    with col_character:
        splitted_documents = split_content(splitter_type="Character", target_url=target_url, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        st.subheader("Character Splitter")
        for splitted_document in splitted_documents:
            st.success(splitted_document.page_content)

    with col_recursive:
        splitted_documents = split_content(splitter_type="Recursive", target_url=target_url, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        st.subheader("Recursive Character Splitter")
        for splitted_document in splitted_documents:
            st.info(splitted_document.page_content)

    with col_semantic:
        splitted_documents = split_content(splitter_type="Semantic", target_url=target_url, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        st.subheader("Semantic Splitter")
        for splitted_document in splitted_documents:
            st.warning(splitted_document.page_content)


