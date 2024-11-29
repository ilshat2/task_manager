

class Task:
    """Класс для представления одной задачи."""

    def __init__(
        self,
        task_id: int,
        name: str,
        description: str,
        category: str,
        due_date: str,
        priority: str,
        status: str = "не выполнена",
    ):
        self.id = task_id
        self.name = name
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def mark_as_completed(self):
        """Отметить задачу как выполненную."""
        self.status = "выполнена"

    def to_dict(self):
        """Преобразовать объект задачи в словарь для сохранения."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }
