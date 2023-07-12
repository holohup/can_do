from api.tools import NewOrder, IdPosition
import pytest


@pytest.mark.parametrize(
        ('old_order', 'new_order', 'expected'),
        (
            (
                [IdPosition(1, 1), IdPosition(2, 2)],
                [2, 1],
                {IdPosition(1, 2), IdPosition(2, 1)}
            ),
            (
                [IdPosition(1, 1), IdPosition(2, 2)],
                [1, 2],
                set()
            ),
            (
                [IdPosition(1, 2), IdPosition(2, 4), IdPosition(5, 7)],
                [1, 5, 2],
                {IdPosition(5, 4), IdPosition(2, 7)}
            ),
            (
                [IdPosition(1, 2), IdPosition(2, 4), IdPosition(5, 7)],
                [2, 5, 1],
                {IdPosition(1, 7), IdPosition(5, 4), IdPosition(2, 2)}
            ),
        )
)
def test_reorder_works(old_order, new_order, expected):
    assert NewOrder(old_order, new_order).reorder() == expected
