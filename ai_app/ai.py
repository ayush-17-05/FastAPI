import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.5-flash")

def ask_ai(prompt: str, system_prompt: str = """You are a helpful assistant. 
Always respond in this exact JSON format:
{"answer": "...", "confidence": "high/medium/low", "follow_up_question": "..."}
""") -> str:
    response = model.generate_content(
        f"{system_prompt}\n\nUser: {prompt}"
    )
    return response.text



#these are system_prompt examples try these and everytime ask the same question like for eg:"what is fastapi?"
#You are a helpful assistant.
#You are a pirate. Answer everything in pirate speak.
#You must answer in exactly one word, nothing else.
#You are a strict senior developer reviewing code. Be critical and point out flaws.
# """You are a helpful assistant. 
# Always respond in this exact JSON format:
# {"answer": "...", "confidence": "high/medium/low", "follow_up_question": "..."}
# """
