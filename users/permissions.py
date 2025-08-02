from rest_framework import permissions

MODERATOR_GROUP_NAME="Moderators"

class IsModerator(permissions.BasePermission):
    """
        Проверка на то, что пользователь модератор.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name=MODERATOR_GROUP_NAME).exists()


class IsOwner(permissions.BasePermission):
    """
        Доступ только владельцу.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrModerator(permissions.BasePermission):
    """
        Доступ владельцу или модератору.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.groups.filter(name=MODERATOR_GROUP_NAME).exists()


class IsNotModerator(permissions.BasePermission):
    """
        Проверка на то, что пользователь не модератор.
    """
    def has_permission(self, request, view):
        return not request.user.groups.filter(name=MODERATOR_GROUP_NAME).exists()
