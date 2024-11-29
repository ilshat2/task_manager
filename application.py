import os
import json
from typing import List, Optional

DATA_FILE = os.path.join(
    os.path.dirname(__file__), "task_manager", "tasks.json"
)


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

    @staticmethod
    def from_dict(data: dict):
        """Создать объект Task из словаря."""
        return Task(
            task_id=data["id"],
            name=data["name"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"],
        )


class TaskManager:
    """Класс для управления списком задач."""

    def __init__(self):
        self.tasks: List[Task] = []
        self.load_tasks()

    def load_tasks(self):
        """Загрузить задачи из файла JSON."""
        try:
            with open(DATA_FILE, "r") as f:
                self.tasks = [Task.from_dict(task) for task in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def save_tasks(self):
        """Сохранить задачи в файл JSON."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    [task.to_dict() for task in self.tasks],
                    f, ensure_ascii=False, indent=4
                )
        except (IOError, TypeError) as e:
            print(f"Ошибка при сохранении задач: {e}")

    def add_task(self, name: str, description: str,
                 category: str, due_date: str, priority: str):
        """Добавить новую задачу."""
        task_id = len(self.tasks) + 1
        task = Task(task_id, name, description, category, due_date, priority)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Задача '{name}' успешно добавлена!")

    def edit_task(self, task_id: int, **kwargs):
        """Редактировать задачу."""
        task = self.find_task_by_id(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key) and value is not None:
                    setattr(task, key, value)
            self.save_tasks()
            print(f"Задача с ID {task_id} успешно обновлена!")
        else:
            print("Задача с указанным ID не найдена.")

    def mark_as_completed(self, task_id: int):
        """Отметить задачу как выполненную."""
        task = self.find_task_by_id(task_id)
        if task:
            task.mark_as_completed()
            self.save_tasks()
            print(f"Задача с ID {task_id} отмечена как выполненная!")
        else:
            print("Задача с указанным ID не найдена.")

    def delete_task(self, task_id: Optional[int] = None,
                    category: Optional[str] = None):
        """Удалить задачу по ID или категории."""
        if task_id:
            self.tasks = [task for task in self.tasks if task.id != task_id]
        elif category:
            self.tasks = [
                task for task in self.tasks if task.category != category]
        self.save_tasks()
        print("Задача(и) успешно удалена(ы)!")

    def view_tasks(self, category: Optional[str] = None):
        """Просмотреть задачи, отфильтровав по категории (если указана)."""
        tasks_to_view = [
            task for task in self.tasks if task.category == category]
        tasks_to_view = tasks_to_view if category else self.tasks
        if tasks_to_view:
            for task in tasks_to_view:
                print(f"""
                    ID: {task.id}
                    Название: {task.name}
                    Категория: {task.category}
                    Срок: {task.due_date}
                    Приоритет: {task.priority}
                    Статус: {task.status}
                """)
        else:
            print("Нет задач для отображения.")

    def search_tasks(self, keyword: Optional[str] = None,
                     category: Optional[str] = None,
                     status: Optional[str] = None):
        """Найти задачи по ключевому слову, категории или статусу."""
        results = self.tasks
        if keyword:
            results = [
                task for task in results if keyword.lower() in task.name.lower()
            ]
        if category:
            results = [task for task in results if task.category == category]
        if status:
            results = [task for task in results if task.status == status]
        if results:
            for task in results:
                print(f"""
                    ID: {task.id}
                    Название: {task.name}
                    Категория: {task.category}
                    Срок: {task.due_date}
                    Приоритет: {task.priority}
                    Статус: {task.status}
                """)
        else:
            print("Нет задач, соответствующих условиям поиска.")

    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        """Найти задачу по ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


def main():
    manager = TaskManager()

    while True:
        print("\nМеню:")
        print("1. Просмотр задач")
        print("2. Добавление задачи")
        print("3. Редактирование задачи")
        print("4. Отметить задачу как выполненную")
        print("5. Удалить задачу")
        print("6. Поиск задач")
        print("0. Выход")

        choice = input("Выберите действие: ")
        if choice == "1":
            category = input("Введите категорию (или оставьте пустым): ")
            manager.view_tasks(category or None)
        elif choice == "2":
            name = input("Название: ")
            description = input("Описание: ")
            category = input("Категория: ")
            due_date = input("Срок выполнения (YYYY-MM-DD): ")
            priority = input("Приоритет (низкий/средний/высокий): ")
            manager.add_task(name, description, category, due_date, priority)
        elif choice == "3":
            task_id = int(input("ID задачи: "))
            name = input("Новое название (или оставьте пустым): ")
            description = input("Новое описание (или оставьте пустым): ")
            category = input("Новая категория (или оставьте пустым): ")
            due_date = input("Новый срок выполнения (или оставьте пустым): ")
            priority = input("Новый приоритет (или оставьте пустым): ")
            manager.edit_task(
                task_id, name=name or None,
                description=description or None,
                category=category or None,
                due_date=due_date or None,
                priority=priority or None
            )
        elif choice == "4":
            task_id = int(input("ID задачи: "))
            manager.mark_as_completed(task_id)
        elif choice == "5":
            task_id = input("ID задачи (или оставьте пустым): ")
            category = input("Категория (или оставьте пустым): ")
            manager.delete_task(
                task_id=int(task_id) if task_id else None,
                category=category or None
            )
        elif choice == "6":
            keyword = input("Ключевое слово: ")
            category = input("Категория: ")
            status = input("Статус (выполнена/не выполнена): ")
            manager.search_tasks(
                keyword or None,
                category or None,
                status or None
            )
        elif choice == "0":
            break
        else:
            print()
            print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
