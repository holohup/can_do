from rest_framework.viewsets import ModelViewSet
from todo.models import Task
from api.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.order_by('position')
    serializer_class = TaskSerializer
