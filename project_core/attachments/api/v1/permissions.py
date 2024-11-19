from rest_framework import permissions


class IsSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_supervisor


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsGetOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True


