import pytest

from todo.models import Task


@pytest.mark.parametrize(
    ('field'),
    (
        'position', 'title', 'description', 'done', 'created_at'
    )
)
@pytest.mark.django_db
def test_task_has_all_the_required_fields(sample_task, field):
    assert hasattr(sample_task, field)


@pytest.mark.django_db
def test_three_tasks_have_positions_1_to_3(sample_task):
    second_task = Task.objects.create()
    third_task = Task.objects.create()
    pos = sample_task.position
    assert second_task.position == pos + 1
    assert third_task.position == pos + 2


@pytest.mark.django_db
def test_if_a_task_is_deleted_new_position_is_largest(sample_task):
    second_task = Task.objects.create()
    third_task = Task.objects.create()
    second_task.delete()
    fourth_task = Task.objects.create()
    assert fourth_task.position == sample_task.position + 3
