import pytest


@pytest.mark.parametrize(
    ('field'),
    (
        'position', 'title', 'description', 'done', 'created_at'
    )
)
@pytest.mark.django_db
def test_task_has_all_the_required_fields(sample_task, field):
    assert hasattr(sample_task, field)
