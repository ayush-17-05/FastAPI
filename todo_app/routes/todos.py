from fastapi import APIRouter, HTTPException,status
import uuid
from typing import Optional
from todo_app.schemas import TodoCreate, TodoOut, TodoUpdate,todo_helper
from todo_app.database import todo_collection
from bson import ObjectId

router=APIRouter(prefix="/api/v1/todos",tags=["todos"])

@router.get("/",response_model=list[TodoOut])
async def get_todos(completed: Optional[bool] = None):
    query = {}
    if completed is not None:
        query["is_completed"] = completed
        
    todos = await todo_collection.find(query).to_list(length=100)
    return [todo_helper(todo) for todo in todos]


@router.post("/",response_model=TodoOut,status_code=status.HTTP_201_CREATED)
async def create_todo(payload: TodoCreate):
    new_todo={
        "title":payload.title,
        "description":payload.description,
        "is_completed":False
    }
    result = await todo_collection.insert_one(new_todo)
    created_todo=await todo_collection.find_one({"_id":result.inserted_id})
    return todo_helper(created_todo)


@router.get("/{todo_id}", response_model=TodoOut)
async def get_todo(todo_id: str):
    todo = await todo_collection.find_one({"_id":ObjectId(todo_id)})
    if todo:
        return todo_helper(todo)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID '{todo_id}' not found",
    )

@router.put("/{todo_id}",response_model=TodoOut)
async def update_todo(todo_id:str, payload:TodoUpdate):
    update_data=payload.dict(exclude_unset=True)

    if update_data:
        await todo_collection.update_one(
            {"_id":ObjectId(todo_id)},{"$set":update_data}
        )
        updated_todo=await todo_collection.find_one({"_id":ObjectId(todo_id)})
        if updated_todo:
            return todo_helper(updated_todo)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID '{todo_id}' not found",
    )
@router.delete("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id:str):
    result=await todo_collection.delete_one({"_id":ObjectId(todo_id)})
    if result.deleted_count == 1:
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID '{todo_id}' not found",
    )


@router.patch("/{todo_id}/complete",status_code=status.HTTP_204_NO_CONTENT)
async def complete_todo(todo_id:str):
    result = await todo_collection.update_one(
        {"_id":ObjectId(todo_id)},
        {"$set":{"is_completed":True}}
    )
    if result.matched_count == 1:
        return
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID '{todo_id}' not found",
    )