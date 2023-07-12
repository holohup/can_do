import pytest
from django.urls import reverse
from rest_framework import status
from todo.models import User
from tests.factories import TaskFactory


@pytest.fixture
def list_response(client):
    url = reverse('tasks-list')
    return client.get(url)


@pytest.fixture
def list_data(client, list_response):
    return list_response.data


@pytest.mark.django_db
def test_api_urls_exist(client):
    assert client.get('/api/').status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_tasks_list_exists(list_response):
    assert list_response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_all_tasks_are_present_in_the_list(task, two_more_tasks, list_data):
    assert len(list_data) == 3


@pytest.mark.django_db
def test_list_contains_only_needed_fields(task, list_data):
    needed_fields = 'id', 'author', 'title', 'description', 'done'
    assert len(list_data[0]) == len(needed_fields)
    for field in needed_fields:
        assert field in list_data[0]


@pytest.mark.django_db
def test_author_doesnt_see_other_authors_tasks(client, two_more_tasks):
    second_author = User.objects.create()
    TaskFactory.create(author=second_author)
    response = client.get(reverse('tasks-list'))
    assert len(response.data) == 2


@pytest.mark.django_db
def test_tasks_are_sorted_correctly(task, two_more_tasks, list_data):
    assert task.id == list_data[0]['id']
    assert two_more_tasks[0].id == list_data[1]['id']
    assert two_more_tasks[1].id == list_data[2]['id']


@pytest.mark.django_db
def test_task_is_created_by_the_authenticated_user(author, client):
    payload = {'title': 'test'}
    response = client.post(reverse('tasks-list'), payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['author'] == author.id
