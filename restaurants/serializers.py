from rest_framework import serializers
from .models import Restaurant
from phonenumber_field.serializerfields import PhoneNumberField
from django.db.models import Q
from menu.serializers import MenuItemSerializer

class RestaurantSerializer(serializers.ModelSerializer):
    name=serializers.CharField(max_length=100, required=True)
    address=serializers.CharField(min_length=15)
    phone_number=PhoneNumberField(required=True)
    pincode = serializers.CharField(max_length=10, required=True)
    menu_items = MenuItemSerializer(many=True, read_only=True) # Nested Serializer

    class Meta:
        model=Restaurant
        fields=['id','owner','name','address','pincode','phone_number','menu_items','created_at','updated_at']
        read_only_fields=['id','owner','created_at','updated_at']

    def validate(self, attrs):
        instance = self.instance

        name = attrs.get('name')
        phone_number = attrs.get('phone_number')
        
        if "name":
            name = name.title()
            attrs["name"] = name

            # Check for duplicate name (excluding current instance during update)
            existing_restaurant = Restaurant.objects.filter(
                Q(name=name)
            ).exclude(id=instance.id if instance else None).exists()  # Exludes the current object/instance being updated
                                                                    # If the instance is different than current exclude id=None
                                                                    # only filtering happens
                                                                     
            if existing_restaurant:     
                raise serializers.ValidationError({"name": "A restaurant with this name already exists!"})

        
        if "phone_number":
            existing_phone = Restaurant.objects.filter(
                Q(phone_number=phone_number)
            ).exclude(id=instance.id if instance else None).exists()

            if existing_phone:
                raise serializers.ValidationError({"phone_number": "This phone number is already registered to another restaurant!"})

        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")

        if request and (not request.user.is_authenticated or request.user.role == "customer"): #possible changes after delivery agent role
            data.pop('created_at', None)
            data.pop('updated_at', None)

        return data
