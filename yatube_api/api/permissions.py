from rest_framework import permissions


class PostAuthorOnly(permissions.BasePermission):
    message = 'Нельзя изменять чужой контент!'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
