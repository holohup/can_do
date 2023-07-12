from itertools import permutations

import pytest
from django.urls import reverse
from rest_framework import status

from tests.factories import TaskFactory
from todo.models import Task, User

REORDER_URL = reverse('tasks-reorder')


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
    needed_fields = 'id', 'title', 'description', 'done'
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


@pytest.mark.django_db
def test_user_cannot_provide_other_authors_id_for_reordering(client, task):
    other_author = User.objects.create()
    other_authors_task = Task.objects.create(author=other_author)
    payload = {'new_order': [task.id, other_authors_task.id]}
    response = client.patch(REORDER_URL, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_author_needs_to_provide_all_order_ids(client, task, two_more_tasks):
    payload = {'new_order': [task.id, two_more_tasks[0].id]}
    response = client.patch(REORDER_URL, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_author_cant_reorder_with_an_empty_list(client):
    payload = {'new_order': []}
    response = client.patch(REORDER_URL, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_author_can_reorder_two_tasks(client, two_more_tasks):
    task_1, task_2 = two_more_tasks
    old_task_1_pos, old_task_2_pos = task_1.position, task_2.position
    payload = {'new_order': [task_2.id, task_1.id]}
    response = client.patch(REORDER_URL, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data['new_order'] == [
        two_more_tasks[1].id, two_more_tasks[0].id
    ]
    task_1.refresh_from_db()
    task_2.refresh_from_db()
    assert task_1.position == old_task_2_pos
    assert task_2.position == old_task_1_pos


@pytest.mark.parametrize(
    ('new_pos'),
    permutations(range(1, 4))
)
@pytest.mark.django_db
def test_three_items_get_reordered_correctly(
    client, task, two_more_tasks, new_pos
):
    tasks = [task] + list(two_more_tasks)
    task_ids = [t.id for t in tasks]
    payload = {'new_order': list(new_pos)}
    response = client.patch(REORDER_URL, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    updated_tasks = Task.objects.filter(id__in=task_ids).order_by(
        'position'
    )
    for i, task in enumerate(updated_tasks):
        assert task.id == new_pos[i]
