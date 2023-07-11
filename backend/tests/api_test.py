import pytest
from django.urls import reverse
from rest_framework import status
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
