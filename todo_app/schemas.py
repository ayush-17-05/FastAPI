from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class TodoCreate(BaseModel):
    title: str=Field(min_length=3,max_length=100)
    description: str=Field(min_length=5,max_length=1000)

class TodoUpdate(BaseModel):
    title: Optional[str]=Field(default=None, max_length=100)
    description: Optional[str]=Field(default=None, max_length=1000)
    is_completed: Optional[bool]=None

class TodoOut(BaseModel):
    id: str
    title: str
    description: str
    is_completed: bool

def todo_helper(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"],
        "is_completed": todo["is_completed"],
    }
