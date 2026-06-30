from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from todo_app.routes.users import get_current_user
from .ai import ask_ai, overall_chain
import google.generativeai as genai
from todo_app.database import conversation_collection
from .tools import run_agent

router=APIRouter()

class AIRequest(BaseModel):
    prompt: str

@router.post("/api/v1/ask")
async def ask(request: AIRequest, current_user: dict = Depends(get_current_user)):
    answer = await ask_ai(request.prompt, current_user["email"], conversation_collection)
    return {"response": answer}

class SummarizeRequest(BaseModel):
    text:str

@router.post("/api/v1/summarize-translate")
async def summarize_translate(request: SummarizeRequest, current_user: dict = Depends(get_current_user)):
    result = overall_chain({"text": request.text})
    return {
        "summary": result["summary"],
        "hindi_translation": result["hindi_translation"]
    }

class AgentRequest(BaseModel):
    query: str

@router.post("/api/v1/agent")
async def agent_endpoint(
    request:AgentRequest,
    current_user:dict=Depends(get_current_user)):
    result = run_agent(request.query)
    return {"response":result}