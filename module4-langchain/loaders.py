#WebBaseLoader - Bir URL'den içerik yükleme
#PyPDFLoader - Bir PDF dosyasından içerik yükleme
#UnstructuredExcelLoader - Bir excel dosyasından içerik yükleme

#Document loaders: farklı tipte dosyaların içindeki veriyi documentlara çevirmek

# WebBaseLoader

# from langchain_community.document_loaders import WebBaseLoader
#
# target_url = "https://kpmg.com/tr/tr/home/insights/2023/12/uretken-yapay-zeka-uygulamalarinin-kurumsallasma-yaklasimi.html"
#
# loader = WebBaseLoader(target_url)
#
# raw_documents = loader.load()
#
# with open("URL_Icerik.txt","w") as file:
#     file.write(raw_documents[0].page_content) #write() string beklediği için listenin ilk elemanını aldık
#
# print("Dosya işlemi tamamlandı.")
#
# print(raw_documents[0].metadata)

#PyPDFLoader - Bir PDF dosyasından içerik yükleme

from langchain_community.document_loaders import PyPDFLoader

# filepath = "/Users/melisacevik/Desktop/Generative-AI/module4-langchain/data/timeline.pdf"

# loader = PyPDFLoader(filepath)
#
# pages = loader.load() #pypdfloader sayfa sayfa listeler halinde döndürür
#
# print(pages[39].page_content, pages[39].metadata)
#
# filepath = "/Users/melisacevik/Desktop/Generative-AI/module4-langchain/data/digital.pdf"
#
# loader = PyPDFLoader(filepath, extract_images=True) # bu pdfteki görseller ayrıştırılsın mı?True : spesifik dosya
# # içindeki spesifik görseli metne çevirebilecek miyiz test et
#
# pages = loader.load()
#
# print(pages[6].page_content)

#UnstructuredExcelLoader - Bir excel dosyasından içerik yükleme

from langchain_community.document_loaders import UnstructuredExcelLoader

# Excel tablomuzu HTML'e çevirelim

filepath = "/Users/melisacevik/Desktop/Generative-AI/module4-langchain/data/ai_course.xlsx"

loader = UnstructuredExcelLoader(filepath, mode="elements") # excel to html yapmak için mode elements parametresi
# giriyoruz

docs = loader.load()

excel_content = docs[0].metadata["text_as_html"]

with open("excel.html","w") as file:
    file.write(excel_content)

