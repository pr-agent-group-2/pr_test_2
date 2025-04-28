
from fastapi import FastAPI, HTTPException
from typing import List
from .models import Todo
from .services import TodoService

app = FastAPI(title="Todo Service", version="0.2.0")
service = TodoService()

@app.get("/todos", response_model=List[Todo])
def list_todos():
    return service.list_todos()

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(item: Todo):
    return service.create_todo(item)

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, item: Todo):
    updated = service.update(todo_id, item)
    if updated is None:
        # At runtime, this will raise because updated is None – intentional for PR Agent to catch
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if not service.delete(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
