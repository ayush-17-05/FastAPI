from fastapi import APIRouter, HTTPException,status
import uuid
from typing import Optional
from todo_app.schemas import TodoCreate, TodoOut, TodoUpdate
from todo_app.storage import save_data,load_data

router=APIRouter(prefix="/api/v1/todos",tags=["todos"])

@router.get("/",response_model=list[TodoOut])
def get_todos(completed: Optional[bool] = None):
    todos=load_data()
    if completed is not None:
        return [todo for todo in todos if todo["is_completed"] == completed]
    return todos

@router.post("/",response_model=TodoOut,status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate):
    todos=load_data()
    new_todo={
        "id":str(uuid.uuid4()),
        "title":payload.title,
        "description":payload.description,
        "is_completed":False
    }
    todos.append(new_todo)
    save_data(todos)
    return new_todo


@router.get("/{todo_id}", response_model=TodoOut)
async def get_todo(todo_id: str):
    todos = load_data()
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID '{todo_id}' not found",
    )

@router.put("/{todo_id}",response_model=TodoOut)
def update_todo(todo_id:str, payload:TodoUpdate):
    todos=load_data()
    for index,todo in enumerate(todos):
        if todo["id"]==todo_id:
            updated_todo=todo.copy()
            if payload.title is not None:
                updated_todo["title"]=payload.title
            if payload.description is not None:
                updated_todo["description"]=payload.description
            if payload.is_completed is not None:
                updated_todo["is_completed"]=payload.is_completed
            todos[index]=updated_todo
            save_data(todos)
            return updated_todo
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID '{todo_id}' not found",
    )

@router.delete("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id:str):
    todos=load_data()
    for index,todo in enumerate(todos):
        if todo["id"]==todo_id:
            todos.pop(index)
            save_data(todos)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID '{todo_id}' not found",
    )


@router.patch("/{todo_id}/complete",status_code=status.HTTP_204_NO_CONTENT)
def complete_todo(todo_id:str):
    todos=load_data()
    for todo in todos:
        if todo["id"]==todo_id:
            todo["is_completed"]=True
            save_data(todos)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID '{todo_id}' not found",
    )