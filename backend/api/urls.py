from rest_framework.routers import DefaultRouter
from django.urls import include, path
from api.views import TaskViewSet


router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')
djoser_urlpatterns = [
    path('auth/', include('djoser.urls'), name='djoser'),
    path('auth/', include('djoser.urls.jwt'), name='jwt')
]

urlpatterns = [
    path('', include(djoser_urlpatterns)),
    path('', include(router.urls)),
]
