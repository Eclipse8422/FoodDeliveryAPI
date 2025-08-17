from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsRestaurantOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.user.is_staff:
            return True
        
        return obj.restaurant.owner == request.user
    
class IsDeliveryAgent(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == "delivery_agent"