from rest_framework.permissions import BasePermission

from clients.utils.permissions import is_manager


class IsOwnerOrManager(BasePermission):
    """Permissions для менеджера. Потльзователь видит только своих клиентов а Менеджер всех"""

    def has_object_permission(self, request, view, obj):
        if is_manager(request.user):
            return True
        return obj.user == request.user
