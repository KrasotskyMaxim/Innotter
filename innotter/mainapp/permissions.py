from rest_framework import permissions


class IsPrivatePage(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_private

class IsFollowerPage(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_private and request.user in obj.followers.all()
    
class IsPageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.page.owner == request.user
    