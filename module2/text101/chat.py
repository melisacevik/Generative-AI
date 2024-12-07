from openai import OpenAI
import os 
from dotenv import load_dotenv

load_dotenv()

my_key = os.getenv("OPENAI_API_KEY") # get the api key from the .env file

# GPT 4-turbo
client = OpenAI(api_key=my_key)

import streamlit as st

#st.chat_input("Mesajınızı Giriniz")

#with st.chat_message("user"):
#    st.markdown("Merhaba")

# karşılıklı olarak alınan ve gönderilen mesajların listesi tutulmalı. chat history => session stage altına yerleştirilmeli
# çünkü widgetlarla etkileşime girdiğimizde sayfa yenilecek ve bu veriler kaybolacak. bu yüzden session state kullanılmalı

if "messages" not in st.session_state:
    st.session_state.messages = [] #sohbet geçmişi oluşturuldu
    st.session_state.messages.append({"role": "system", "content":"Sen yardımsever bir asistansın"})

# bir sohbet geçmişi için ilk oluşturulacak mesaj sistem mesajı olmalı. bu mesajı oluşturduktan sonra kullanıcıdan bir mesaj alınmalı
# sistem mesajı oluşturuldu ve sohbet geçmişine eklendi

# promptları biz vereceğiz. yanıtları ise openai verecek. bu yüzden bir metod oluşturulmalı ve bu metod çağrıldığında prompt sohbet geçmişine eklenmeli

def generate_response(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})

#böylelikle bu metodun çağrıldığı her yerde,  kendisine verilen prompt bizim sohbet geçmişimize bir kullanıcı mesajı olarak eklenmiş olacak

    AI_Response = client.chat.completions.create(
        model = "gpt-4-1106-preview",
        messages=st.session_state.messages
    )

    return AI_Response.choices[0].message.content

# AI kodları tamamlandı.

# Şimdi Streamlit arayüzü oluşturulacak

st.header("👾 Chat with Melisa 💜")
st.divider()

# [1:] yapmamızın sebebi, sohbet geçmişinin ilk elemanının sistem mesajı olması ve bu mesajın ekrana yazdırılmaması gerektiğinden [1:]
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# := operatörü şu işe yarar: sağdaki ifadeyi değerlendirir ve sol taraftaki değişkene atar. Eğer sağdaki ifade bir değer döndürüyorsa bu değeri atar. Eğer döndürmüyorsa bu durumda hata verir. 
# bu kod bloğu input alanına bir değer girildiğinde ve gönderildiğinde çalışacak.

if prompt := st.chat_input("Mesajınızı Giriniz"):

    st.chat_message("user").markdown(prompt)

    response = generate_response(prompt) # yazdığımız metni modele gönder ve yanıtı response değişkenine ata

    with st.chat_message("assistant"): # karşıdan aldığımız değeri asistan markdownı ile chat mesajına ekle
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response}) # sohbet geçmişine eklenen mesajı asistan mesajı olarak ekle


