from rest_framework.viewsets import ModelViewSet
from todo.models import Task
from api.serializers import TaskSerializer, ReorderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class TaskViewSet(ModelViewSet):
    """A viewset for tasks, including the reordering endpoint."""

    serializer_class = TaskSerializer
    http_method_names = ('get', 'post', 'patch')

    @action(('patch',), detail=False)
    def reorder(self, request):
        context = {
            'request': request,
            'tasks': self.get_queryset()
        }
        serializer = ReorderSerializer(
            instance=self.get_queryset(),
            data=request.data,
            partial=True,
            context=context
        )
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user).order_by(
            'position'
        )
