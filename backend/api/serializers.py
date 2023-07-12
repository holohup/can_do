from rest_framework import serializers
from todo.models import Task
from rest_framework.exceptions import ValidationError


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'author', 'title', 'description', 'done')
        read_only_fields = ('id', 'position', 'created_at', 'author')


class ReorderSerializer(serializers.ModelSerializer):
    new_order = serializers.ListField(write_only=True, allow_empty=False)

    class Meta:
        model = Task
        fields = ('new_order',)

    # def to_internal_value(self, data):
    #     print('!!!'*30, data)
    #     return super().to_internal_value(data)

    def validate_new_order(self, data):
        user = self.context['request'].user
        user_tasks = Task.objects.filter(author=user)
        user_task_ids = [task.id for task in user_tasks]
        for _id in data:
            if _id not in user_task_ids:
                raise ValidationError(
                    f'You cannot reoder tasks from other people: {_id}')
        if len(data) != len(user_tasks):
            raise ValidationError(
                'You need to provide all of your tasks to reorder')
        return data

    # def save(self, **kwargs):
    #     print('save')
    #     return super().save(**kwargs)

    # def to_representation(self, instance):
    #     print(self.context['request'])
    #     return super().to_representation(instance)
