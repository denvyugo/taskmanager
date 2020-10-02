from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsUser
from . import serializers
from . import models


class TaskViewset(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated, IsUser]
    filterset_fields = {
        'status': ['exact'],
        'plan': ['exact', 'lte', 'gte', 'isnull']
    }
