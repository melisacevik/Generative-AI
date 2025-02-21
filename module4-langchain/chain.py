# # 1. Zincir :
# Create Stuff Documents Chain
#
# from langchain_openai import ChatOpenAI #Langchain içerisinden ChatOpenAI sınıfını kullanmak ve llm'e erişmek için dahil edildi.(GPT4 ile konuşmamızı sağlayacak)
# from langchain_core.documents import Document #Retrieval işlemi (bellek genişletme) yaparken alınan ve verilen verileri genelde bu documents sınıfına göre formatlandırırız.
# from langchain_core.prompts import ChatPromptTemplate #İşlemleri hızlandırır.
# from langchain.chains.combine_documents import create_stuff_documents_chain
#
# # Document sınıfının 2 temel özelliği var. Aslında bu sınıf bir veri modeli. Veriye giydirilen şablon.
# # Document.page_content : Asıl veriyi tutarız
# # Document.metadata : O veriyle ilgili ek bilgileri tutarız. (nereden geldiği, veri tipi, uzunluğu vs.)
#
import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# my_key_openai = os.getenv("openai_apikey")
#
# llm = ChatOpenAI(model="gpt-4-0125-preview",api_key=my_key_openai)
#
# # Bu zincirden (create_stuff_documents_chain), ham veriden bazı çıkarımlar yapmasını bekleyeceğiz.
# # Dil modeline bir soru yöneltirken onun işini kolaylaştırmak için bu soruyla alakalı olabilecek bazı ek bilgiler vermeye bellek genişletme denir.
# # Zincirin rolü, birden çok farklı türdeki nesneyi biraraya getirip çalışmaya yarayacak.
#
#
# # Amaç şu: Document'in içeriğini alıp incele, promptta sorduğum soruya uygun bir şekilde yanıt üret.
# # Bunları zincir halinde yapılacak.
#
#
# # 2. promptu hazırla
# # ChatPromptTemplate.from_messages : string builder işlemini yapar.
#
# prompt = ChatPromptTemplate.from_messages(
#     [("system", "Burada ismi geçen kişilerin en sevdiği rengi tek tek yaz:\n\n{context}")]
# )
#
# # context: isimler olarak geçiyor
#
# #1. doc'u hazırla
# docs = [
#     Document(page_content="Melisa kırmızıyı sever ama sarıyı sevmez"),
#     Document(page_content="Çağrı yeşili sever ama maviyi sevdiği kadar değil"),
#     Document(page_content="Burak'a sorsan favori rengim yok der ama belli ki turuncu rengini seviyor")
# ]
#
# #3. chain'i hazırla
#
# chain_1 = create_stuff_documents_chain(llm,prompt)
#
# #docu chaini aktif ettiğimiz yerde kullanacağız. bunun için invoke() kullanırız. contexti de burada kullanırız.
#
# print(chain_1.invoke({"context": docs}))

# 2. Zincir

# Create OpenAI Function Runnable Chain
# OpenAI'in GPT modelleri ile birlikte sağladığı fonksiyon çağırma özelliğini yerine getiren bir zincirdir.

from langchain_openai import ChatOpenAI # LLM Olarak GPT'den yararlanmak için kullandığımız sınıf
from langchain_core.prompts import ChatPromptTemplate #Promptu düzenlemek için kullandığımız sınıf
from pydantic import BaseModel, Field #pydantic: veri biçimlendirme kütüphanesi
from typing import Optional # Sınıfın bazı özelliklerinin zorunlu bazılarının opsiyonel old. durumlarda kullanılır.
from langchain.chains.structured_output.base import create_openai_fn_runnable #Kullanacağımız zincir

# Problem: Yapılandırılmamış ham veride, bu ham veri içerisinden belirli veri biçimine uygun çıkarımlar yapılmak isteniyor.
# Diyalog metninden insanların bahsettiği diğer kişilerin belirli özelliklerini (isim,yaş,meslek) anlayıp bir sınıfa atamaya çalışalım.
# Bu konuşmada geçen şehirlerle ilgili kısmı (şehir ismi, plaka no, iklimi) şehir adındaki bir sınıfa atayacağız.

# HAM VERİDEN YAPILANDIRILMIŞ VARLIKLAR  (Structured entity) ÇIKARACAĞIZ.

# 1. Classları tanımla

# Insan sınıfı kalıtım yoluyla BaseModel sınıfından türetiliyor

import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("openai_apikey")

class Insan(BaseModel):
    """ Bir insan hakkında tanımlayıcı bilgiler"""
    isim: str = Field(..., description="Kişinin ismi") #... = doldurmak zorunlu demek(null olamaz)
    yas: int = Field(..., description="Kişinin yaşı")
    meslek: Optional[str] = Field(None, description="Kişinin mesleği") #optional = null veya null değil fark etmez o yüzden None

class Sehir(BaseModel):
    """ Bir şehir hakkında tanımlayıcı bilgiler"""

    isim: str = Field(..., description="Şehrin ismi")
    plaka_no: str = Field(..., description="Şehrin plaka numarası")
    iklim: Optional[str] = Field(None, description="Şehrin iklimi")

llm = ChatOpenAI(
    model="gpt-4-turbo",
    api_key=my_key_openai
)

# langchainde system user yerine system human key i kullanılıyor. user = human
# input : dışardan veri gelmesini sağlayacak
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Sen varlıkları kaydetmek konusunda dünyanın en başarılı algoritmasısın."),
        ("human", "Şu verdiğim girdideki varlıkları kaydetmek için gerekli fonksiyonlara çağrı yap: {input}"),
        ("human", "İpucu: Doğru formatta yanıtladığına emin ol")
    ]
)

chain_2 = create_openai_fn_runnable([Insan, Sehir],llm,prompt)

print(chain_2.invoke({"input": "Aydın 34 yaşında başarılı bir bilgisayar mühendisiydi."}))
print(chain_2.invoke({"input": "Aydın'da hava her zaman sıcak ve bu yüzden 89 plakalı araçlarda klima hep çalışır."}))

