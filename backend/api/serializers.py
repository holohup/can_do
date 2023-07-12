from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.tools import IdPosition, NewOrder
from todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for basic tasks actions."""

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'done')
        read_only_fields = ('id', 'position', 'created_at')


class ReorderSerializer(serializers.Serializer):
    """Serializer for reordering."""

    new_order = serializers.ListField(write_only=True, allow_empty=False)

    def validate_new_order(self, data):
        user_task_ids = [task.id for task in self._tasks]
        for _id in data:
            if _id not in user_task_ids:
                raise ValidationError(
                    f'You cannot reoder tasks from other people: {_id}')
        if len(data) != len(self._tasks):
            raise ValidationError(
                'You need to provide all of your tasks to reorder')
        if len(data) != len(set(data)):
            raise ValidationError(
                'A task cannot occupy two places in a list'
            )
        return data

    def update(self):
        current_positions = [
            IdPosition(task.id, task.position) for task in self._tasks
        ]
        new_positions = self.validated_data['new_order']
        positions_to_update = NewOrder(
            current_positions, new_positions
        ).reorder()
        ids_to_clean = set(t.id for t in positions_to_update)
        tasks_to_update = Task.objects.filter(id__in=ids_to_clean)
        update_list = []
        with transaction.atomic():
            tasks_to_update.update(position=None)
            for id_pos in positions_to_update:
                task = tasks_to_update.get(id=id_pos.id)
                task.position = id_pos.pos
                update_list.append(task)
            Task.objects.bulk_update(update_list, ['position'])

        return self.instance

    def to_representation(self, inst):
        return {'new_order': [task.id for task in inst.order_by('position')]}

    @property
    def _tasks(self):
        return self.context['tasks']
