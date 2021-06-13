from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from users.models import Profile


class IsAdminOnly(permissions.BasePermission):
    """
    Allows access only to admin or django_admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
                return True
            try:
                return request.user.profile.role == 'admin'
            except:
                return False

        return False


class IsUser(permissions.BasePermission):
    '''
    Allows access to moderator make patch requests
    '''

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.role == 'user' and request.method in SAFE_METHODS
        return False