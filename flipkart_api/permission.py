from rest_framework import permissions


class CustomAdminPermissions(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # admin_permissions = bool(request.user and request.user.is_staff)
        # return request.method == 'GET' or admin_permissions
    
        if request.method in permissions.SAFE_METHODS: # get method is safe method
            return True
        else:
            return bool(request.user and request.user.is_staff)
    
    
class ReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user == request.user