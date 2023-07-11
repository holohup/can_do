import pytest

from todo.models import Task


@pytest.mark.parametrize(
    ('field'),
    (
        'position', 'title', 'description', 'done', 'created_at'
    )
)
@pytest.mark.django_db
def test_task_has_all_the_required_fields(task, field):
    assert hasattr(task, field)


@pytest.mark.django_db
def test_three_tasks_have_positions_1_to_3(task, two_more_tasks):
    second_task, third_task = two_more_tasks
    pos = task.position
    assert second_task.position == pos + 1
    assert third_task.position == pos + 2


@pytest.mark.django_db
def test_new_task_position_doesnt_get_inserted_in_a_wrong_position(
    task, author, two_more_tasks
):
    second_task, _ = two_more_tasks
    second_task.delete()
    fourth_task = Task.objects.create(author=author)
    assert fourth_task.position == task.position + 3
