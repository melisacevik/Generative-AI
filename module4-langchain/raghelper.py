from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings # rag için embeddinglere ihtiyacımız var
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS #facebookun servisi, Kullanacığımız metinleri vektör olarak
# kullanmamızı sağlayacak
from langchain_cohere import CohereEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter #metinleri belirli yerden böler
import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_google = os.getenv("google_apikey")
my_key_hf = os.getenv("huggingface_access_token") #read tipinde oluşturduk

llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-1.5-flash")

#embeddings = OpenAIEmbeddings(api_key=my_key_openai)

#embeddings = CohereEmbeddings(cohere_api_key=my_key_cohere, model="embed-multilingual-v3.0") #embed-englist-v3.0

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# Gemini ile olan iletişimi sağlamak için ask_gemini()
def ask_gemini(prompt):

    AI_Response = llm_gemini.invoke(prompt)

    return AI_Response.content

# Web adresi üzerinde bellek genişletme işlemi için rag_with_url()
def rag_with_url(target_url, prompt):

    loader = WebBaseLoader(target_url)

    raw_documents = loader.load() #laoder ile işlenmemiş dokümanlar oluştu. bunlara erişmek için raw_documents
    # oluşturduk. (Liste halinde gelir). YÜKLEDİK. Şimdi sırada bölümlemede.

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len
    )

    splitted_documents = text_splitter.split_documents(raw_documents) #yüklenen dokümanlar bölümleniyor.

    vectorstore = FAISS.from_documents(splitted_documents, embeddings) #FAISS'in from_documents() metodu => metinlerden vektör
    # elde ediyor. FAISS , splitted_documents verisini embeddingse göre vektörlere çeviriyor.

    retriever = vectorstore.as_retriever() #getiriciye çeviriyoruz.

    relevant_documents = retriever.get_relevant_documents(prompt) # promptla ilgili olduğunu bildiğimiz bazı ek bilgiler

    # amaç => prompt ve relevant documents ı, llme göndericez. promptu verip buna vereceğin yanıtı burada ara dicez(
    # retrieverda )

    #relevant documents liste olarak döner o yüzden ara işlem yapalım. prompt string istediği için,
    # stringe çevirmeliyiz. (veriyi arka arkaya yazıp stringe çeviriyoruz)

    context_data = ""

    for document in relevant_documents:
        context_data += " " + document.page_content

    final_prompt = f"""Şöyle bir sorum var: {prompt}
    Bu soruyu yanıtlamak için elimizde şu bilgiler var: {context_data}.
    Bu sorunun yanıtını vermek için yalnızca sana burada verdiğim eldeki bilgileri kullan. Bunların dışına asla 
    çıkma."""

    AI_Response = llm_gemini.invoke(final_prompt)

    return AI_Response.content


# Pdf üzerinde bellek genişletme işlemi için rag_with_pdf()
def rag_with_pdf(file_path, prompt):

    loader = PyPDFLoader(file_path)

    raw_documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len
    )

    splitted_documents = text_splitter.split_documents(raw_documents)

    vectorstore = FAISS.from_documents(splitted_documents, embeddings)

    retriever = vectorstore.as_retriever()

    relevant_documents = retriever.get_relevant_documents(prompt)

    context_data = ""

    for document in relevant_documents:
        context_data += " " + document.page_content

    final_prompt = f"""Şöyle bir sorum var: {prompt}
    Bu soruyu yanıtlamak için elimizde şu bilgiler var: {context_data}.
    Bu sorunun yanıtını vermek için yalnızca sana burada verdiğim eldeki bilgileri kullan. Bunların dışına asla 
    çıkma."""

    AI_Response = llm_gemini.invoke(final_prompt)

    return AI_Response.content, relevant_documents
