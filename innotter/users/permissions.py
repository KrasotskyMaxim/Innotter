from rest_framework import permissions
from users.models import User 


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.ADMIN
    
    def has_object_permission(self, request, view, obj):
        return request.user.role == User.Roles.ADMIN


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.MODERATOR
    
    def has_object_permission(self, request, view, obj):
        return request.user.role == User.Roles.MODERATOR


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.USER 
    
    def has_object_permission(self, request, view, obj):
        return request.user.role == User.Roles.USER
    

class IsBlockedUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_blocked

    def has_permission(self, request, view):
        return request.user.is_blocked
    