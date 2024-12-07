from openai import OpenAI
import streamlit as st
import requests
from io import BytesIO
import base64
import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("OPENAI_API_KEY")
my_key_stabilityai = os.getenv("STABILITYAI_API_KEY")

client = OpenAI(
    api_key=my_key_openai
)

#DALL-E 3 Image Generation

def generate_image(prompt):

    AI_Response = client.images.generate(
        model = "dall-e-3",
        size = "1024x1024",
        quality="hd",
        n=1,
        response_format="url",
        prompt=prompt
    )

    image_url = AI_Response.data[0].url
    revised_prompt = AI_Response.data[0].revised_prompt

    response = requests.get(image_url)
    image_bytes = BytesIO(response.content)

    return image_bytes, revised_prompt

#DALL-E 3 Variation

def create_image_variation(source_image_file):
    AI_Response = client.images.create_variation(
        image=source_image_file,  # Dosyayı doğrudan buraya aktar
        size="1024x1024",
        n=1,
        response_format="url"
    )

    generated_image_url = AI_Response.data[0].url

    response = requests.get(generated_image_url)
    image_bytes = BytesIO(response.content)

    return image_bytes

#SD XL Image Generation
import time

def generate_with_SD(prompt):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {my_key_stabilityai}",
    }

    body = {
        "steps": 40,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "cfg_scale": 5,
        "samples": 1,
        "text_prompts": [
            {
                "text": prompt,
                "weight": 1
            },
            {
                "text": "blurry, bad",
                "weight": -1
            }
        ],
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    try:
        data = response.json()
        # Yanıtı kontrol etmek için ekrana yazdır
        print("API Yanıtı:", data)
        return data
    except Exception as e:
        print("Hata: Yanıt JSON formatında değil.")
        print(response.text)  # Ham yanıtı yazdır
        return {}


tab_generate,tab_variation, tab_SD = st.tabs(["Resim Üret", "Varyasyon Oluştur", "Stable Diffusion"])

with tab_generate:
    st.subheader("DALL-E 3 ile Görsel Oluşturma")
    st.divider()
    prompt = st.text_input("Oluşturmak istediğiniz görseli tarif ediniz")
    generate_btn = st.button("Oluştur")

    if generate_btn:
        image_data, revised_prompt = generate_image(prompt)

        st.image(image=image_data)
        st.divider()
        st.caption(revised_prompt)

with tab_variation:
    st.subheader("DALL-E 3 ile Görsel Varyasyonu Oluşturma")
    st.divider()
    selected_file = st.file_uploader("PNG formatında bir görsel seçiniz", type=["png"])

    if selected_file:
        # Yüklenen dosyayı Streamlit üzerinden göstermek için içerik kullanılır
        st.image(image=selected_file)

        variation_btn = st.button("Varyasyon Oluştur")

        if variation_btn:
            # Bellekteki dosyayı doğrudan kullanmak için `selected_file` açılır
            image_data = create_image_variation(selected_file)

            # Üretilen varyasyonu göster
            st.image(image=image_data)

with tab_SD:
    st.subheader("Stable Diffusion ile Görsel Oluşturma")
    st.divider()
    SD_prompt = st.text_input("Oluşturmak istediğiniz görseli tarif ediniz", key="sd_text_input")
    SD_generate_btn = st.button("Oluştur", key="sd_button")

    if SD_generate_btn:
        data = generate_with_SD(SD_prompt)


        for image in data["artifacts"]:
            image_bytes = base64.b64decode(image["base64"])
            st.image(image=image_bytes)


# Stable diffusion => debug