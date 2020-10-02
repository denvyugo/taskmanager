import pytest
from task_utils import Task, User

@pytest.fixture
def get_user():
    user = User()
    return user

def test_register(get_user):
    """register new user"""
    user = get_user
    user.register('user1', 'p4s$w0Rd')
    assert user.id == 1


def test_login_logout(get_user):
    """login user"""
    user = get_user
    user.loging('user1', 'p4s$w0Rd')
    assert user.token is not None
    user.logout()
    assert user.token is None

    
