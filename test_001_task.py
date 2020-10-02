import pytest
from datetime import datetime as dt, timedelta
from task_utils import Task, User


@pytest.fixture
def get_user():
    user = User()
    user.loging('user1', 'p4s$w0Rd')
    return user


def test_new_task(get_user):
    """new task"""
    user = get_user
    assert user.token is not None
    task = Task(user, 'todo_001')
    task.description = 'no description'
    user.add_task(task)
    assert task.status == 'NEW'


def test_get_task(get_user):
    """get task"""
    user = get_user
    task = user.task_by_id(1)
    assert task.name == 'todo_001'
    task.plan = dt.today() + timedelta(days=1)
    task.status = 'PLN'
    user.save_task(task)


def test_update(get_user):
    """test update"""
    user = get_user
    task = user.task_by_id(1)
    assert task.status == 'PLN'

def test_filter(get_user):
    user = get_user
    task = Task(user, 'todo_002')
    task.description = 'new task'
    user.add_task(task)
    planed_tasks = user.get_tasks_status(status='PLN')
    planed_task = planed_tasks[0]
    assert planed_task.status == 'PLN'
