from typing import List
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import select, Session
from app.database import init_db, get_session
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate

app = FastAPI(title="Todo API", version="1.0.0")
init_db()

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(data: TodoCreate, session: Session = Depends(get_session)):
    todo = Todo(title=data.title, description=data.description or "")
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.get("/todos", response_model=List[Todo])
def list_todos(offset: int = 0, limit: int = Query(default=10, le=100),
               session: Session = Depends(get_session)):
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(404, "Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, data: TodoUpdate, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(404, "Todo not found")
    update_data = data.dict(exclude_unset=True)
    for k, v in update_data.items():
        setattr(todo, k, v)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(404, "Todo not found")
    session.delete(todo)
    session.commit()
