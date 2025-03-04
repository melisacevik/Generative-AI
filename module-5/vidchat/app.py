#videohelper ile youtube videolarını metne dönüştürdük
#youtube_video ile youtube videolarının standart ve belirli bir formatta kullanılması için
#raghelper ile bu metinler üzerinde rag tabanlı altyapı oluşturduk

import streamlit as st
import videohelper
import raghelper

if "current_video_url" not in st.session_state:
    st.session_state.current_video_url = None
    st.session_state.current_transcript_docs = []

st.set_page_config(page_title="VidChat: YouTube ile Sohbet", layout="centered")
st.image(image="/Users/melisacevik/Generative-AI/module-5/vidchat/img/app_banner.png")
st.title("VidChat: YouTube ile Sohbet")
st.divider()

tab_url,tab_search = st.tabs(["URL Girerek", "Arama Yaparak"])

with tab_url:
    video_url = st.text_input(label="YouTube Video Adresini Giriniz:", key="url_video_url")
    prompt = st.text_input(label="Sorunuzu Giriniz:", key="url_prompt")
    submit_btn = st.button("Sor", key="url_submit")

    if submit_btn:
        st.video(data=video_url)
        st.divider()
        if st.session_state.current_video_url != video_url:
            #Aşama 1: video -> audio -> text
            #Aşama 2: text -> bellek genişletme

            # Aşama1:
            with st.spinner("AŞAMA-1: Video metni hazırlanıyor..."):
                video_transcript_docs = videohelper.get_video_transcript(url=video_url)
                st.session_state.current_transcript_docs = video_transcript_docs
        st.success("Video transkripti ön belleğe kaydedildi!")
        st.divider()
        # elde ettiğimiz veriyi saklamak ve daha sonra tekrar kullanmak için (zaman, maliyet) yerelde saklarız: caching
        st.session_state.current_video_url = video_url

        with st.spinner("AŞAMA-2: Sorunuz yanıtlanıyor..."):
            AI_Response, relevant_documents = raghelper.rag_with_video_transcript(
                transcript_docs=st.session_state.current_transcript_docs, prompt=prompt)
        st.info("YANIT:")
        st.markdown(AI_Response)
        st.divider()

        for doc in relevant_documents:
            st.warning("REFERANS:")
            st.caption(doc.page_content)
            st.markdown(f"Kaynak: {doc.metadata}")
            st.divider()













