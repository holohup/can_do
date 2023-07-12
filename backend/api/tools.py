from typing import NamedTuple

from rest_framework.exceptions import ValidationError


class IdPosition(NamedTuple):
    """Human-friendly task id and position tuple."""

    id: int
    pos: int


class NewOrder:
    """Class to find out what has changed.
    Also provides a method that returns of what id's need a position update."""

    def __init__(
            self,
            old_order: list[IdPosition],
            new_order: list[int]
    ) -> None:
        self._old_order = old_order
        self._new_order = new_order
        self._validate()

    def _validate(self):
        if len(self._new_order) != len(self._old_order):
            raise ValidationError('Can not reorder - the lists are different')

    def reorder(self) -> set[IdPosition]:
        result = set()
        for i in range(len(self._new_order)):
            id = self._new_order[i]
            pos = self._old_order[i].pos
            if self._old_order[i].id == id:
                continue
            result.add(IdPosition(id, pos))
        return result
