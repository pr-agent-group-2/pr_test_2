
from typing import List
from .models import Todo

class TodoService:
    """In‑memory storage service for Todo items."""

    def __init__(self):
        self._todos: List[Todo] = []
        self._id_counter: int = 1

    def list_todos(self) -> List[Todo]:
        return self._todos

    def create_todo(self, item: Todo) -> Todo:
        item.id = self._id_counter
        self._id_counter += 1
        self._todos.append(item)
        return item
