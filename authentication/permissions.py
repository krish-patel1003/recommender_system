from rest_framework import permissions


class IsRecommenderSystemAdmin(permissions.BasePermission):
    

    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_admin