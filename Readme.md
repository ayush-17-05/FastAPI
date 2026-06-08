python -m venv .venv
.\.venv/Scripts/activate

https://devsheets.io/sheets/fastapi

pip install "fastapi[standard]"

pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port $PORT

