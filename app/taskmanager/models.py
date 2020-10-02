from django.conf import settings
from django.db import models


class Task(models.Model):
    """model for user's task"""
    NEW = 'NEW'
    PLANING = 'PLN'
    WORKING = 'WRK'
    COMPLETE = 'CMP'
    TASK_STATUS_CHOICES = [
        (NEW, 'Новая'),
        (PLANING, 'Запланированная'),
        (WORKING, 'В работе'),
        (COMPLETE, 'Завершена'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=3,
                              choices=TASK_STATUS_CHOICES, default=NEW)
    plan = models.DateField(null=True)
