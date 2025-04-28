
"""Todo service with rudimentary persistence (intentionally imperfect).

* Adds update and delete operations.
* Introduces a subtle bug: duplicate IDs are possible after deletion because the counter is not decremented.
"""
from typing import List, Optional
from .models import Todo

class TodoService:
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

    def get(self, todo_id: int) -> Optional[Todo]:
        return next((t for t in self._todos if t.id == todo_id), None)

    def update(self, todo_id: int, data: Todo) -> Optional[Todo]:
        todo = self.get(todo_id)
        if todo:
            todo.title = data.title or todo.title
            todo.completed = data.completed
        # BUG: returning None instead of the updated instance breaks FastAPI validation
        return None

    def delete(self, todo_id: int) -> bool:
        before = len(self._todos)
        self._todos = [t for t in self._todos if t.id != todo_id]
        return len(self._todos) != before
