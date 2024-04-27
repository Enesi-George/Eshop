from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from django.contrib.auth.models import AnonymousUser

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.role=='admin' 

class CanCreateSuperAdmin(permissions.BasePermission):
    """Allows access only to admin users."""

    def has_permission(self, request, view):
        return request.user.is_staff and request.user.has_perm('api.add_appadminuser')

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role=='admin' or request.user.is_staff and request.user.is_active   

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff    

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user
