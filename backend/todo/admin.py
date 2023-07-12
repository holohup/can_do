from django.contrib import admin
from django.contrib.auth.models import Group

from todo.models import Task

admin.site.unregister(Group)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin panel for the tasks."""

    list_display = (
        'id',
        'author',
        'title',
        'description',
        'done',
        'created_at',
    )
    list_editable = ('done',)
