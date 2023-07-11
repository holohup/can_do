from rest_framework import serializers
from todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'author', 'title', 'description', 'done')
        read_only_fields = ('id', 'position', 'created_at')
