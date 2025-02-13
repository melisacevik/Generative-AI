import os
from dotenv import load_dotenv

load_dotenv()

# 1. OPENAI -GPT-
my_key_openai = os.getenv("openai_apikey")

from langchain_openai import ChatOpenAI

def ask_gpt(prompt, temperature, max_tokens):

    llm = ChatOpenAI(api_key=my_key_openai, temperature=temperature, max_tokens=max_tokens, model="gpt-4-1106-preview")

    AI_Response = llm.invoke(prompt)

    return AI_Response.content

# 2. Google -GEMINI-
my_key_google = os.getenv("google_apikey")

from langchain_google_genai import ChatGoogleGenerativeAI

def ask_gemini(prompt, temperature):
    llm = ChatGoogleGenerativeAI(google_api_key=my_key_google, temperature=temperature, model="gemini-pro")

    AI_Response = llm.invoke(prompt)

    return AI_Response.content

#ANTHROPIC -Claude-

my_key_antropic = os.getenv("cohere_apikey")

import anthropic

# def ask_claude(prompt, temperature, max_tokens):
#
#     llm = ChatAnthropic(anthropic_api_key=my_key_antropic,
#                         temperature=temperature,
#                         max_tokens=max_tokens,
#                         model="claude-2.1")
#
#     AI_Response = llm.invoke(prompt)
#
#     return AI_Response.content
#

# COHERE -Command-
# my_key_cohere = os.getenv("cohere_apikey")
#
# from langchain_community.chat_models import ChatCohere
#
# def ask_command(prompt, temperature, max_tokens):
#
#     llm = ChatCohere(cohere_api_key=my_key_cohere, temperature=temperature,
#                      max_tokens=max_tokens, model="command")
#
#     AI_Response = llm.invoke(prompt)
#
#     return AI_Response.content

# 3. DEEPSEEK
from openai import OpenAI

my_key_deepseek = os.getenv("deepseek_apikey")

client = OpenAI(api_key=my_key_deepseek, base_url="https://api.deepseek.com")

def ask_deepseek(prompt,temperature,max_tokens):
    response = client.chat.completions.create(
        model="deepseek-chat",
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False
    )

    return response.choices[0].message.content




