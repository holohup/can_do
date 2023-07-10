from django.db import models
from django.utils import timezone


class Task(models.Model):
    position = models.IntegerField(
        'Position in list', unique=True, null=False, db_index=True)
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description', blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
