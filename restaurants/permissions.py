from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False

        return obj.owner == request.user or request.user.role == "admin"
    