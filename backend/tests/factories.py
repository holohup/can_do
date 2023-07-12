from factory import Faker
from factory.django import DjangoModelFactory

from todo.models import Task


class TaskFactory(DjangoModelFactory):
    def __init__(self, author) -> None:
        self.author = author
        super().__init__()

    class Meta:
        model = Task

    title = Faker('word')
    description = Faker('text')
    done = Faker('boolean')
