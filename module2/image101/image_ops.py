from openai import OpenAI
import streamlit as st
import requests # urldeki resmi çekmek için.
from io import BytesIO # urldeki resmi yerele taşımak için.
import base64 # resmi base64 formatına çevirmek için.
import os 
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_stabilityai = os.getenv("stabilityai_apikey")

st.set_page_config(page_title="Chat with Melisa 💜", page_icon=":heart:")

client = OpenAI(
    api_key = my_key_openai
)

#DALL-E 3 Imagine Generation

def generate_image(prompt):
    AI_Response = client.images.generate(
        model = "dall-e-3",
        size = "1024x1024",
        quality="hd",
        n=1,
        response_format="url",
        prompt=prompt
    )

    image_url = AI_Response.data[0].url # AI tarafından oluşturulan resmin url'si
    revised_prompt = AI_Response.data[0].revised_prompt # AI tarafından oluşturulan resmin tarifi

    response = requests.get(image_url)
    image_bytes = BytesIO(response.content)

    return image_bytes, revised_prompt

#DALL-E 3 Variation

def create_image_variation(source_image_url):

    AI_Response = client.images.create_variation(
        image=open (source_image_url, "rb"),
        size="1024x1024",
        n=1,
        response_format="url"
    )

    generated_image_url = AI_Response.data[0].url

    response = requests.get(generated_image_url)
    image_bytes = BytesIO(response.content)

    return image_bytes

#SD XL Image Generation

#stabilityai 'in SDK sini kullanmayacağız. kendi http requeestimizi yazacağız.

def generate_with_SD(prompt):

    # ulaşacağımız sunucunun adresini(urlsini) belirleyelim
    # biz bu çağrıları hangi web adresindeki hangi sunucunun hangi endpointine göndereceğiz?

    #url : nereye gidiyoruz
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    #headers : body'nin hangi formatta olduğunu belirleyelim. oraya erişmeye yetkimiz var mı?

    headers = {
        "Accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {my_key_stabilityai}",
    }
    #body : göndermek istediğimiz verileri belirleyelim. ne götürüyoruz ( en zoru )
    body = {
        "steps":40, #difüzyon sürecinin kaç adım sürmesini istediğimizi belirler.
        "width":1024, #oluşturulacak görselin genişliği
        "height":1024, #oluşturulacak görselin yüksekliği
        "seed": 0, #oluşturulacak görselin kimliği
        "cfg_scale":5, #modele verilen ölçeklendirme faktörü. yapay zekanın sınırlarını belirler. serbest bırakmak için 1, sıkılaştırmak için 10 kullanılır.
        "samples":1, #kaç tane görsel oluşturulacağını belirler.
        "text_promps":[
            {
                "text":prompt,
                "weight":1,
            },
            { #neleri görmek istemediğimizi belirleriz. 2. bir text_promps ekleyerek negatif örnekler veririz.
                "text":"blurry,bad",
                "weight":-1 #negatif olduğu için -1. 
            }
        ],        
    }

    #karşı tarafa nasıl göndermek istediğimizi belirleyelim.

    response = requests.post(url, headers=headers, json=body)

    # bu isteği gönderdikten sonra bize ne döndüğünü görelim.

    data = response.json()

    return data

    # şimdi tab_SD kısmında bu fonksiyonu kullanacağız.

# frontend tarafı

tab_generate,tab_variation, tab_SD = st.tabs(["Resim Üret", "Varyasyon Oluştur","Stable Diffusion"])

with tab_generate:
    st.subheader("DALL-E ile Görsel Oluşturma")
    st.divider()
    prompt = st.text_input("Oluşturmak istediğiniz görseli tarif edin.")
    generate_btn = st.button("Görsel Oluştur")

    if generate_btn:
        image_data, revised_prompt = generate_image(prompt)

        st.image(image = image_data)
        st.divider()
        st.caption(revised_prompt)

with tab_variation:
    st.subheader("DALL-E ile Görsel Varyasyonu Oluşturma")
    st.divider()
    selected_file = st.file_uploader("PNG formatında bir görsel seçiniz.", type=["png"])
    
    if selected_file:
        st.image(image=selected_file.name)

    variation_btn = st.button("Varyasyon Oluştur")

    if variation_btn:
        image_data = create_image_variation(selected_file.name)
        st.image(image=image_data)

with tab_SD:
    st.subheader("Stable Diffusion ile Görsel Oluşturma")
    st.divider()
    prompt_sd = st.text_input("Oluşturmak istediğiniz görseli tarif edin.", key="prompt_sd")
    sd_btn = st.button("Görsel Oluştur", key="sd_button")

    if sd_btn:
        data = generate_with_SD(prompt_sd)

        for image in data["artifacts"]:
            image_bytes = base64.b64decode(image["base64"])
            st.image(image=image_bytes)
            

# son sayfa üzerinde çalış!

