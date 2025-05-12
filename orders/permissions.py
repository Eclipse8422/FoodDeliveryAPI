from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsRestaurantOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.user.is_staff:
            return True
        
        return obj.restaurant.owner == request.user