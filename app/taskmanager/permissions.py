from rest_framework import permissions


class IsUser(permissions.BasePermission):
    message = 'No an user'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
