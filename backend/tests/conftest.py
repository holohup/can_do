from todo.models import Task
import pytest


@pytest.fixture
def sample_task():
    return Task.objects.create(position=1)
