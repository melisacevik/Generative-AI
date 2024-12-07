import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

my_key = os.getenv("GOOGLE_APIKEY")

genai.configure(
    api_key=my_key
)

client = genai.GenerativeModel(
    model_name="gemini-pro"
)

AI_Response = client.generate_content(
    "Mevsimler neden oluşur?",
    generation_config=genai.GenerationConfig(
        temperature=0,
        max_output_tokens=256
    )
)

print(AI_Response.text)