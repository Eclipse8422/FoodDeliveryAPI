from rest_framework import serializers
from .models import User
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.validators import ValidationError
from django.db.models import Q

class UserCreationSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=40)
    email=serializers.EmailField(max_length=80)
    phone_number=PhoneNumberField(required=True)
    password=serializers.CharField(min_length=8, write_only=True)
    role=serializers.ChoiceField(choices=User.ROLE_CHOICES, default="customer")

    class Meta: 
        model=User
        fields=['username','email','phone_number','password','role']

    def validate(self,attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')

        existing_user = User.objects.filter(
            Q(username=username) | Q(email=email) | Q(phone_number=phone_number)
        ).first()

        if existing_user:
            if existing_user.username == username:
                raise ValidationError({"username": "User with this username already exists!"})
            if existing_user.email == email:
                raise ValidationError({"email": "User with this email already exists!"})
            if existing_user.phone_number == phone_number:
                raise ValidationError({"phone_number": "User with this phone number already exists!"})
            
        return attrs
    
    def validate_role(self,value):
        allowed_roles=['customer','restaurant_owner'] #possible changes after delivery agent added
        if value not in allowed_roles:
            raise serializers.ValidationError("You can only register as a customer or a restaurant owner!")
        
        return value
    
    '''
    Required as default create method does not hash passwords,
    so we use create_user function defined in CustomUserManager Class.
    '''
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)