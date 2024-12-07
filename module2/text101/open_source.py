import replicate
from dotenv import load_dotenv

load_dotenv()

prompt = "Mevsimler nasıl oluşur?"
system_prompt = "Sen yardımsever bir asistansın"

# Llama 2

AI_Response = replicate.run(
    "meta/llama-2-70b-chat",
    input = {
        "temperature": 0.5,
        "max_new_tokens": 256,
        "system_prompt": system_prompt,
        "prompt": prompt,
        "debug": False
    }
)

AI_Response = "".join(AI_Response) # düz metine çevirmek için

print(AI_Response)

print("*" * 100)

# Mistral

AI_Response = replicate.run(
    "mistralai/mistral-7b-v0.1",
    input = {
        "temperature": 0.5,
        "max_new_tokens": 256,
        "system_prompt": system_prompt,
        "prompt": prompt,
        "debug": False
    }
)

AI_Response = "".join(AI_Response) # düz metine çevirmek için

print(AI_Response)