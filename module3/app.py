import streamlit as st
import threading
import time
import importlib
import transcripter
import painter

# Uygulama baştan başlatıldığında doğru şekilde set etme
if "record_active" not in st.session_state:
    st.session_state.record_active = threading.Event()  # Ses kaydına başlarken ve biterken kontrol edilecek
    st.session_state.recorder_status = "Başlamaya Hazırız!"
    st.session_state.recording_completed = False
    st.session_state.latest_image = ""
    st.session_state.message = []
    st.session_state.frames = []
    st.session_state.messages = []
    st.session_state.recorder_module = None  # Recorder modülünü geçici olarak burada tutacağız

# Recorder modülünü geç yükleme
def load_recorder_module():
    if st.session_state.recorder_module is None:
        st.session_state.recorder_module = importlib.import_module("recorder")
        st.session_state.recorder_status = "🎤 **Recorder Modülü Yüklendi**"

# Kayıt başlatma fonksiyonu
def start_recording():
    load_recorder_module()  # Recorder modülünü burada yüklüyoruz
    st.session_state.record_active.set()
    st.session_state.frames = []
    st.session_state.recorder_status = "🔴 **Sesiniz Kaydediliyor...**"
    st.session_state.recording_completed = False

    threading.Thread(
        target=st.session_state.recorder_module.record,
        args=(st.session_state.record_active, st.session_state.frames)
    ).start()

# Kayıt durdurma fonksiyonu
def stop_recording():
    st.session_state.record_active.clear()
    st.session_state.recorder_status = "✅ **Kayıt Tamamlandı**"
    st.session_state.recording_completed = True

# Streamlit sayfa ayarları
st.set_page_config(page_title="VoiceDraw", layout="wide", page_icon="/Users/melisacevik/Desktop/Generative-AI/module3/icons/app_icon.png")
st.image(image="/Users/melisacevik/Desktop/Generative-AI/module3/icons/top_banner.png", use_container_width=True)
st.title("VoiceDraw: Sesli Çizim")
st.divider()

# Ses Kayıt Bölümü
col_audio, col_image = st.columns([1, 2])

with col_audio:
    st.subheader("Ses Kayıt")
    st.divider()

    status_message = st.info(st.session_state.recorder_status)
    st.divider()

    subcol_left, subcol_right = st.columns([1, 4])

    with subcol_left:
        start_btn = st.button(label="Başlat", on_click=start_recording, disabled=st.session_state.record_active.is_set())
        stop_btn = st.button(label="Durdur", on_click=stop_recording, disabled=not st.session_state.record_active.is_set())

    with subcol_right:
        recorded_audio = st.empty()

        if st.session_state.recording_completed:
            recorded_audio.audio(data="voice_prompt.wav")

    st.divider()
    latest_image_use = st.checkbox("Son resmi kullan")

# Görsel Çıktı Bölümü
with col_image:
    st.subheader("Görsel çıktılar")
    st.divider()

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(name=message["role"], avatar="/Users/melisacevik/Desktop/Generative-AI/module3/icons/ai_avatar.png"):
                st.warning("İşte sizin için oluşturduğum görsel: ")
                st.image(image=message["content"], width=300)
        elif message["role"] == "user":
            with st.chat_message(name=message["role"], avatar="/Users/melisacevik/Desktop/Generative-AI/module3/icons/user_avatar.png"):
                st.success(message["content"])

# Kayıt tamamlandıysa transkripsiyon ve görsel oluşturma işlemleri
if stop_btn:
    with st.chat_message(name="user", avatar="/Users/melisacevik/Desktop/Generative-AI/module3/icons/user_avatar.png"):
        with st.spinner("Sesiniz Çözümleniyor..."):
            voice_prompt = transcripter.transcribe_with_whisper(audio_file_name="voice_prompt.wav")
        st.success(voice_prompt)

    st.session_state.messages.append({"role": "user", "content": voice_prompt})

    with st.chat_message(name="assistant", avatar="/Users/melisacevik/Desktop/Generative-AI/module3/icons/ai_avatar.png"):
        st.warning("İşte sizin için oluşturduğum görsel: ")

        with st.spinner("Görseliniz oluşturuluyor..."):
            if latest_image_use:
                image_file_name = painter.generate_image(image_path=st.session_state.latest_image, prompt=voice_prompt)
            else:
                image_file_name = painter.generate_image_with_dalle(prompt=voice_prompt)

        st.image(image=image_file_name, width=300)

        with open(image_file_name, "rb") as file:
            st.download_button(
                label="Resmi İndir",
                data=file,
                file_name=image_file_name,
                mime="image/png"
            )

    st.session_state.messages.append({"role": "assistant", "content": image_file_name})
    st.session_state.latest_image = image_file_name
