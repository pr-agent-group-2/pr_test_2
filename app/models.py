
from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    completed: bool = False
