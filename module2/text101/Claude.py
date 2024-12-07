import anthropic
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

my_key = os.getenv("ANTHROPIC_APIKEY")

client = anthropic.Anthropic(
    api_key=my_key
)

def generate_response(prompt):
    AI_Response = client.beta.messages.create(
        model="claude-2.1",
        temperature=0,
        max_tokens=256,
        messages=[
            {"role":"user", "content":prompt}
        ]
    )

    return AI_Response.content[0].text

st.header("Claude ile İletişim Kurma")
st.divider()

prompt = st.text_input("Mesajınızı giriniz")
submit_btn = st.button("Gönder")

if submit_btn:
    response = generate_response(prompt)
    st.markdown(response)


# api key alındığında çok rahat çalışıyor
