from todo.models import User
import pytest
from tests.factories import TaskFactory


@pytest.fixture
def author():
    return User.objects.create()


@pytest.fixture
def task(author):
    return TaskFactory.create(author=author)


@pytest.fixture
def two_more_tasks(author):
    return (
        TaskFactory.create(author=author), TaskFactory.create(author=author)
    )
