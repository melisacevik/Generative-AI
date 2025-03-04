# videohelper sayesinde oluşturulmuş transcript içeriğini (metinsel içeriği) yapay zeka modeli ile kuracağımız
# iletişimde rag aracı olarak
# kullanacağız. çünkü dil modeline soracağımız soruları dil modelinin kendi eğitim verisi ile değil ilgili videomuzun
# içeriğinden yola çıkarak cevaplamasını istiyoruz. bu yüzden bu bileşeni(raghelperı) oluşturduk.


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
#embeddinglerden oluşturulmuş vektörlerin bir vektorstore de tutulması ve benzerlik kıyaslaması yapılması için
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_google = os.getenv("google_apikey")

llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-1.5-flash")

embeddings = OpenAIEmbeddings(api_key=my_key_openai)

#1 Dil Modeli ile Konuşma

def ask_gemini(prompt):

    AI_Response = llm_gemini.invoke(prompt)

    return AI_Response.content


#2 Bellek Genişletme Süreci + video transcript metinleri

def rag_with_video_transcript(transcript_docs,prompt):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len #chunck size kullanılırken len metodunu kullanalım
    )

    #diğer projelerde önce loader.load yapmıştık ama burada gerek yok (zaten yaptık get_video_transcriptte)

    splitted_documents = text_splitter.split_documents(transcript_docs)

    vectorstore = FAISS.from_documents(splitted_documents, embeddings)

    retriever = vectorstore.as_retriever()

    relevant_documents = retriever.get_relevant_documents(prompt)

    context_data = ""

    for document in relevant_documents:
        context_data += " " + document.page_content


    final_prompt = f"""Şöyle bir sorum var: {prompt}
    Bu soruyu yanıtlamak için elimizde şu bilgiler var: {context_data} .
    Bu sorunun yanıtını vermek için yalnızca sana burada verdiğim eldeki bilgileri kullan. Bunların dışına asla çıkma.
    """

    AI_Response = ask_gemini(final_prompt)

    return AI_Response, relevant_documents


