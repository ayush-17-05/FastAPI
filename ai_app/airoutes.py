from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from todo_app.routes.users import get_current_user
from .ai import ask_ai
import google.generativeai as genai

router=APIRouter()

class AIRequest(BaseModel):
    prompt: str

@router.post("/api/v1/ask")
async def ask(request: AIRequest, current_user: dict = Depends(get_current_user)):
    answer = ask_ai(request.prompt)
    return {"response": answer}