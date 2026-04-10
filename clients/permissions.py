from rest_framework.permissions import BasePermission


class IsOwnerOrManager(BasePermission):
    """Permissions для менеджера. Потльзователь видит только своих клиентов а Менеджер всех"""

    def has_object_permission(self, request, view, obj):
        if request.user.role == "manager":
            return True
        return obj.user == request.user
