from rest_framework import serializers
from .models import DeliveryAgent
from rest_framework.serializers import ValidationError


class DeliveryAgentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DeliveryAgent
        fields = ['id', 'user', 'pincode', 'is_available', 'is_approved', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'is_approved', 'created_at', 'updated_at']


    def validate_user(self, value):
        if value.role != "delivery_agent":
            raise ValidationError("Only users with role 'delivery_agent' can be registered as delivery agents.")
        return value
    
    def validate_pincode(self, value):
        if not value.isdigit() or len(value) != 6:
            raise ValidationError("Pincode must be a 6-digit number!")
        return value
        
    def validate_is_approved(self, value):
        # This checks whether the delivery user sends is_approved as True
        if self.context.get("request").method == "POST" and value:
            raise ValidationError("New delivery agents cannot be approved upon creation. Admin approval is required.")
        
        return value
        
    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user if request else None

        #  (POST) because while updating we dont want this validation error
        if request.method ==  "POST":
            if hasattr(user, 'delivery_agent'):
                raise ValidationError(("You have already registered as a delivery agent."))
            
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request and request.user.role == "delivery_agent":
            data.pop('created_at', None)
            data.pop('updated_at', None)

        return data