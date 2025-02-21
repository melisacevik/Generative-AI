import streamlit as st
import raghelper

st.set_page_config(page_title="LangChain ile Bellek Genişletme", layout="wide")

st.title("LangChain ile Bellek Genişletme: URL")
st.divider()

col_input, col_rag, col_normal = st.columns([1,2,3])

with col_input:
    target_url = st.text_input(label="İşlenecek Web Adresinizi Giriniz")
    st.divider()
    prompt = st.text_input(label="Sorunuzu giriniz:", key="url_prompt")
    st.divider()
    submit_btn = st.button("Sor", key="url_button")
    st.divider()

    if submit_btn:

        with col_rag:
            with st.spinner("Yanıt Hazırlanıyor..."):
                st.success("YANIT - Bellek Genişletme Devrede")
                st.markdown(raghelper.rag_with_url(target_url=target_url, prompt=prompt))
                st.divider()

        with col_normal:
            with st.spinner("Yanıt Hazırlanıyor..."):
                st.info("YANIT - Bellek Genişletme Devre Dışı")
                st.markdown(raghelper.ask_gemini(prompt=prompt))
                st.divider()

st.title("LangChain ile Bellek Genişletme: PDF")
st.divider()

col_input, col_rag, col_normal = st.columns([1,2,3])

with col_input:
    selected_file = st.file_uploader(label="İşlenecek dosyayı seçiniz", type=["pdf"])
    st.divider()
    prompt = st.text_input(label="Sorunuzu giriniz:", key="pdf_prompt")
    st.divider()
    submit_btn = st.button("Sor", key="pdf_button")
    st.divider()

    if submit_btn:

        with col_rag:
            with st.spinner("Yanıt Hazırlanıyor..."):
                st.success("YANIT - Bellek Genişletme Devrede")
                AI_Response, relevant_documents = raghelper.rag_with_pdf(file_path=f"./module4-langchain/data/"
                                                                                   f"{selected_file.name}", prompt=prompt)
                st.markdown(AI_Response)
                st.divider()
                for doc in relevant_documents:
                    st.caption(doc.page_content)
                    st.markdown(f"Kaynak: {doc.metadata}")
                    st.divider()

        with col_normal:
            with st.spinner("Yanıt Hazırlanıyor..."):
                st.info("YANIT - Bellek Genişletme Devre Dışı")
                st.markdown(raghelper.ask_gemini(prompt=prompt))
                st.divider()