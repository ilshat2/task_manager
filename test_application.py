import pytest
import unittest
from unittest.mock import patch
from io import StringIO
from application import TaskManager


@pytest.fixture
def task_manager():
    """Фикстура для создания экземпляра TaskManager перед каждым тестом."""
    manager = TaskManager()
    manager.tasks = []  # Очистить задачи перед каждым тестом
    return manager


def test_add_task(task_manager):
    """Тест добавления задачи."""
    task_manager.add_task(
        "Test Task",
        "Description",
        "Work",
        "2024-12-01",
        "высокий"
    )

    assert len(task_manager.tasks) == 1

    task = task_manager.tasks[0]

    assert task.name == "Test Task"
    assert task.category == "Work"
    assert task.priority == "высокий"
    assert task.status == "не выполнена"


def test_edit_task(task_manager):
    """Тест редактирования задачи."""
    task_manager.add_task(
        "Test Task",
        "Description",
        "Work", "2024-12-01",
        "высокий"
    )
    task_id = task_manager.tasks[0].id
    task_manager.edit_task(task_id, name="Updated Task", priority="низкий")
    task = task_manager.find_task_by_id(task_id)
    assert task.name == "Updated Task"
    assert task.priority == "низкий"


def test_mark_as_completed(task_manager):
    """Тест пометки задачи как выполненной."""
    task_manager.add_task(
        "Test Task",
        "Description",
        "Work",
        "2024-12-01",
        "высокий"
    )
    task_id = task_manager.tasks[0].id
    task_manager.mark_as_completed(task_id)
    task = task_manager.find_task_by_id(task_id)

    assert task.status == "выполнена"


def test_delete_task_by_id(task_manager):
    """Тест удаления задачи по ID."""
    task_manager.add_task(
        "Test Task",
        "Description",
        "Work",
        "2024-12-01",
        "высокий"
    )
    task_id = task_manager.tasks[0].id
    task_manager.delete_task(task_id=task_id)

    assert len(task_manager.tasks) == 0


def test_delete_task_by_category(task_manager):
    """Тест удаления задач по категории."""
    task_manager.add_task(
        "Test Task 1",
        "Description",
        "Work",
        "2024-12-01",
        "высокий"
    )
    task_manager.add_task(
        "Test Task 2",
        "Description",
        "Personal",
        "2024-12-02",
        "средний"
    )
    task_manager.delete_task(category="Work")

    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].category == "Personal"


def test_search_task_by_keyword(task_manager):
    """Тест поиска задач по ключевому слову."""
    task_manager.add_task(
        "Test Task",
        "Description",
        "Work",
        "2024-12-01",
        "высокий"
    )
    task_manager.add_task(
        "Another Task",
        "Description",
        "Work",
        "2024-12-02",
        "средний"
    )

    with patch('sys.stdout', new=StringIO()) as fake_out:
        task_manager.search_tasks(keyword="Test")
        output = fake_out.getvalue().strip()

    assert "Test Task" in output
    assert "Another Task" not in output


def test_search_task_by_category(task_manager):
    """Тест поиска задач по категории."""
    task_manager.add_task(
        "Test Task",
        "Description",
        "Work",
        "2024-12-01",
        "высокий"
    )
    task_manager.add_task(
        "Another Task",
        "Description",
        "Personal",
        "2024-12-02",
        "средний"
    )

    with patch('sys.stdout', new=StringIO()) as fake_out:
        task_manager.search_tasks(category="Personal")
        output = fake_out.getvalue().strip()

    assert "Another Task" in output
    assert "Test Task" not in output


def test_search_task_by_status(task_manager):
    """Тест поиска задач по статусу выполнения."""
    task_manager.add_task(
        "Test Task",
        "Description",
        "Work",
        "2024-12-01",
        "высокий"
    )
    task_id = task_manager.tasks[0].id
    task_manager.mark_as_completed(task_id)

    with patch('sys.stdout', new=StringIO()) as fake_out:
        task_manager.search_tasks(status="выполнена")
        output = fake_out.getvalue().strip()

    assert "Test Task" in output


@patch('builtins.open', unittest.mock.mock_open(
    read_data='[{"id": 1, "name": "Test Task", "description": "Description", "category": "Work", "due_date": "2024-12-01", "priority": "высокий", "status": "не выполнена"}]'
))
def test_load_tasks(task_manager):
    """Тестируем загрузку задач."""
    task_manager.load_tasks()


@patch('builtins.open', unittest.mock.mock_open())
def test_save_tasks(task_manager):
    """Тестируем сохранение задач."""
    task_manager.save_tasks()


if __name__ == '__main__':
    pytest.main()
