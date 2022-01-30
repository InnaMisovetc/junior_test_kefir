from rest_framework import permissions


class AdministrationPermission(permissions.BasePermission):
    message = 'You do not have permission to perform this action'

    def has_permission(self, request, view):
        return request.user.is_admin
