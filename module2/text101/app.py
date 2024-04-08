from openai import OpenAI
import os 
from dotenv import load_dotenv

load_dotenv()

my_key = os.getenv("openai_apikey") # get the api key from the .env file

client = OpenAI(api_key=my_key)

AI_Response = client.chat.completions.create(
    model = "gpt-4-1106-preview",
    temperature=0,
    max_tokens=256,
    messages=[
        {"role": "system", "content":"Sen yardımsever bir asistansın"},
        {"role": "user", "content": "Mevsimler neden oluşur? Dünya kendi etrafında döndüğü için mi?"}
    ]
)

print(AI_Response.choices[0].message.content)