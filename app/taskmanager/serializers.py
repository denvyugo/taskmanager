from rest_framework import serializers
from . import models


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Task
        fields = ('id', 'name', 'description',
                  'created', 'status', 'plan', 'user')
