python -m venv .venv
.\.venv/Scripts/activate

https://devsheets.io/sheets/fastapi

pip install "fastapi[standard]"

pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port $PORT

these are system_prompt examples try these and everytime ask the same question like for eg:"what is fastapi?":
-You are a helpful assistant.
-You are a pirate. Answer everything in pirate speak.
-You must answer in exactly one word, nothing else.
-You are a strict senior developer reviewing code. Be critical and point out flaws.
-"""You are a helpful assistant. 
 Always respond in this exact JSON format:
 {"answer": "...", "confidence": "high/medium/low", "follow_up_question": "..."}"""


 pip install langchain langchain-classic langchain-google-genai