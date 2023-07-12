from todo.models import User
import pytest
from tests.factories import TaskFactory
from rest_framework.test import APIClient


@pytest.fixture
def author():
    author = User.objects.create(username='test_user')
    author.set_password('test_password')
    author.save()
    return author


@pytest.fixture
def client(author):
    c = APIClient()
    c.force_authenticate(user=author)
    return c


@pytest.fixture
def task(author):
    return TaskFactory.create(author=author)


@pytest.fixture
def two_more_tasks(author):
    return (
        TaskFactory.create(author=author), TaskFactory.create(author=author)
    )
