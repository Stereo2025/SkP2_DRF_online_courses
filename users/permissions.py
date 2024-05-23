from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()
