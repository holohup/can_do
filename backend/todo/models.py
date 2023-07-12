from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    """Model for tasks."""

    position = models.IntegerField(
        'Position in list',
        unique=True,
        null=True,
        db_index=True,
    )
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description', blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Increments the position if a new task is being created."""

        if self.__class__.objects.exists():
            current_max_position = self.__class__.objects.latest(
                'position'
            ).position
        else:
            current_max_position = 0
        if not self.pk:
            self.position = current_max_position + 1
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.id} - {self.title}'
