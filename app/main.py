
from fastapi import FastAPI
from typing import List
from .models import Todo
from .services import TodoService

app = FastAPI(title="Todo Service", version="0.1.0")
service = TodoService()

@app.get("/todos", response_model=List[Todo])
def list_todos():
    """Return all todos."""
    return service.list_todos()

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(item: Todo):
    """Create a new todo item."""
    return service.create_todo(item)
