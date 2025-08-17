from rest_framework.permissions import BasePermission

class IsApprovedDeliveryAgent(BasePermission):
    
    message = "You must be an approved delivery agent to perform this action."

    def has_permission(self, request, view):
        user = request.user

        if (
            user.is_authenticated and 
            hasattr(user, 'delivery_agent') and 
            user.role == 'delivery_agent' and 
            user.delivery_agent.is_approved
        ):
            return True

        return False