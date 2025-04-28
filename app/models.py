
from pydantic import BaseModel, Field
from typing import Optional
import datetime as _dt

class Todo(BaseModel):
    id: Optional[int] = Field(default=None, description="Auto‑generated ID")
    title: str = Field(..., max_length=120, description="Title of the task")
    completed: bool = False
    created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
