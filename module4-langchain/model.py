import streamlit as st
import modelhelper
import time

st.set_page_config(page_title="LangChain: Model Karşılaştırma", layout="wide")
st.title("LangChain: Model Karşılaştırma")
st.divider()

col_prompt, col_settings = st.columns([2,3]) #[2,3] sütunlara ayırdığımız alan

with col_prompt:
    prompt = st.text_input("Sorunuzu giriniz:")
    st.divider()
    submit_btn = st.button("Sor")

with col_settings:
    temperature = st.slider(label="Temperature",min_value=0.0, max_value=1.0, value=0.7) #min,max,value aynı türde olmalı.
    max_tokens = st.slider(label="Maximum Tokens", min_value=100,value=200,step=100)

st.divider()

col_gpt, col_gemini, col_deepseek = st.columns(3)

with col_gpt:
    if submit_btn:
        with st.spinner("GPT Yanıtlıyor..."):
            st.success("GPT-4 Turbo")
            start_time = time.perf_counter() #işlem öncesi
            st.write(modelhelper.ask_gpt(prompt=prompt, temperature=temperature, max_tokens=max_tokens))
            end_time = time.perf_counter() #işlem sonrası
            elapsed_time = end_time - start_time
            st.caption(f"|  :hourglass: {round(elapsed_time)} saniye")

with col_gemini:
    if submit_btn:
        with st.spinner("Gemini Yanıtlıyor..."):
            st.info("Gemini Pro")
            start_time = time.perf_counter() #işlem öncesi
            st.write(modelhelper.ask_gemini(prompt=prompt, temperature=temperature))
            end_time = time.perf_counter() #işlem sonrası
            elapsed_time = end_time - start_time
            st.caption(f"|  :hourglass: {round(elapsed_time)} saniye")

# with col_claude:
#     if submit_btn:
#         with st.spinner("Claude Yanıtlıyor..."):
#             st.error("Claude 2.1")
#             start_time = time.perf_counter() #işlem öncesi
#             st.write(modelhelper.ask_claude(prompt=prompt, temperature=temperature, max_tokens=max_tokens))
#             end_time = time.perf_counter() #işlem sonrası
#             elapsed_time = end_time - start_time
#             st.caption(f"|  :hourglass: {round(elapsed_time)} saniye")

# with col_command:
#     if submit_btn:
#         with st.spinner("Command Yanıtlıyor..."):
#             st.warning("Command")
#             start_time = time.perf_counter() #işlem öncesi
#             st.write(modelhelper.ask_command(prompt=prompt, temperature=temperature, max_tokens=max_tokens))
#             end_time = time.perf_counter() #işlem sonrası
#             elapsed_time = end_time - start_time
#             st.caption(f"|  :hourglass: {round(elapsed_time)} saniye")
with col_deepseek:
    if submit_btn:
        with st.spinner("Deepseek Yanıtlıyor..."):
            st.error("Deepseek Chat")
            start_time = time.perf_counter() #işlem öncesi
            st.write(modelhelper.ask_gpt(prompt=prompt, temperature=temperature, max_tokens=max_tokens))
            end_time = time.perf_counter() #işlem sonrası
            elapsed_time = end_time - start_time
            st.caption(f"|  :hourglass: {round(elapsed_time)} saniye")