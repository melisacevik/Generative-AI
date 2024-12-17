from openai import OpenAI
import assemblyai as aai
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("OPENAI_API_KEY")
my_key_assemblyai = os.getenv("ASSEMBLYAI_API_KEY")

client = OpenAI(api_key=my_key_openai)

def create_speech_text(prompt,speech_file_name, voice_type="alloy"):

    AI_response = client.audio.speech.create(
        model="tts-1",
        voice=voice_type,
        response_format="mp3",
        input=prompt
    )

    #karşıdan gelen yanıt ses dosyası olacak. gelen ses dosyasını kendi local dosyamıza stream edeceğiz.

    AI_response.stream_to_file(speech_file_name)

    return "Seslendirme başarılı"

def transcribe_with_whisper(audio_file):
    AI_generated_transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="tr",
    )
    return AI_generated_transcript.text

def translate_with_whisper(audio_file):
    AI_generated_translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file
    )
    return AI_generated_translation.text

def transcribe_with_conformer(audio_file_name):
    aai.settings.api_key = my_key_assemblyai
    transcriber = aai.Transcriber()

    AI_generated_text = transcriber.transcribe(audio_file_name)
    return AI_generated_text.text

# streamlit arayüzünü oluştur

tab_TTS, tab_whisper, tab_translation= st.tabs(
    [
        "TTS İle Ses Sentezleme",
        "Whisper ile Transkripsiyon",
        "Whisper ile Tercüme"
    ]
)

# ilk tab ile başlıyoruz.

with tab_TTS:
    st.subheader("TTS-1 Modeli İle Konuşma Sentezleme")
    st.divider()

    # kullanıcıdan alınacak bir metni seslendireceğiz.

    prompt = st.text_input("Seslendirmek istediğiniz metni girin", key="prompt_tts")
    voices = ["alloy","echo","fable","onyx","nova","shimmer"]
    voice_type= st.selectbox(label="Ses tercihini seçin", options=voices, key="voice_tts")
    generate_btn = st.button("Seslendir", key="button_tts")

    # butona tıklandığında API çağrısı göndermeli
    if generate_btn:
        status = create_speech_text(prompt=prompt, speech_file_name="output.mp3", voice_type=voice_type)
        st.success(status)

        audio_file = open("output.mp3", "rb")
        audio_bytes = audio_file.read()

        st.audio(data=audio_bytes, format="audio/mp3")
        st.balloons()

# 2. tab işitsel bazlı bir veriyi metne çevirme : transkripsiyon

with tab_whisper:
    st.subheader("Whisper ile Transkripsiyon")
    st.divider()

    # Kullanıcıdan ses dosyası yüklemesi istenir
    selected_file = st.file_uploader("Bir ses dosyası yükleyin", type=["mp3"], key="file_whisper")

    if selected_file:
        # Bellekteki dosyayı oku ve ses olarak Streamlit'te çal
        audio_bytes = selected_file.read()
        st.audio(data=audio_bytes, format="audio/mp3")

        transcribe_btn = st.button("Metne Dönüştür", key="button_whisper")

        if transcribe_btn:
            # Bellekteki dosyayı doğrudan fonksiyona gönder
            generated_text = transcribe_with_whisper(audio_file=selected_file)

            st.divider()
            st.info(f"TRANSKRIPSİYON: {generated_text}")
            st.balloons()

# 3. tab işitsel bazlı bir veriyi metne çevirme : tercüme

with tab_translation:
    st.subheader("Whisper ile Tercüme")
    st.divider()

    # Kullanıcıdan ses dosyası yüklemesi istenir
    selected_file = st.file_uploader("Bir ses dosyası yükleyin", type=["mp3"], key="file_translation")

    if selected_file:
        # Bellekteki dosyayı oku ve ses olarak Streamlit'te çal
        audio_bytes = selected_file.read()
        st.audio(data=audio_bytes, format="audio/mp3")

        translate_btn = st.button("Tercüme et", key="button_translation")

        if translate_btn:
            # selected_file nesnesini fonksiyona geçirin
            translated_text = translate_with_whisper(audio_file=selected_file)

            st.divider()
            st.info(f"Tercüme: {translated_text}")
            st.balloons()

# 4. tab conformer modeli ile transkripsiyon

# with tab_conformer:
#     st.subheader("Conformer Modeli ile Transkripsiyon")
#     st.divider()
#
#     # Kullanıcıdan ses dosyası yüklemesi istenir
#     selected_file = st.file_uploader("Bir ses dosyası yükleyin", type=["mp3"], key="file_conformer")
#
#     if selected_file:
#         # Bellekteki dosyayı oku ve ses olarak Streamlit'te çal
#         audio_bytes = selected_file.read()
#         st.audio(data=audio_bytes, format="audio/mp3")
#
#         transcribe_btn = st.button("Metne Dönüştür", key="button_conformer")
#
#         if transcribe_btn:
#             # Geçici dosya oluştur ve AssemblyAI ile kullan
#             with open("temp_audio.mp3", "wb") as temp_file:
#                 temp_file.write(selected_file.getbuffer())
#                 # AssemblyAI'ye gönderirken dosya yolunu kullan
#                 generated_text = transcribe_with_conformer(audio_file_name="temp_audio.mp3")
#
#             st.divider()
#             st.info(f"TRANSKRIPSİYON: {generated_text}")
#             st.balloons()

