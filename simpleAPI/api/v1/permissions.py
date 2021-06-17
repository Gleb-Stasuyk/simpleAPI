from rest_framework import permissions

from companys.models import Company


class IsAdminOnly(permissions.BasePermission):
    """
    Allows access only to admin or django_admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                return request.user.profile.role == 'admin'
            except:
                return request.user.is_superuser

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            try:
                return request.user.profile.role == 'admin'
            except:
                return request.user.is_superuser

        return False

class IsUser(permissions.BasePermission):
    '''
    Allows access to moderator make patch requests
    '''

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                return request.user.profile.role == 'user' and request.method in ['GET', 'PATCH', "PUT"]
            except AttributeError:
                return False
        return False

    def has_object_permission(self, request, view, obj):
        if obj == request.user.profile.company:
            return True
        return False

