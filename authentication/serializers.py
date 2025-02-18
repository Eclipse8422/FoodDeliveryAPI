from rest_framework import serializers
from .models import User
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.validators import ValidationError

class UserCreationSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=40)
    email=serializers.EmailField(max_length=80)
    phone_number=PhoneNumberField()
    password=serializers.CharField(min_length=8, write_only=True)

    class Meta: 
        model=User
        fields=['username','email','phone_number','password']

    def validate(self,attrs):
        if User.objects.filter(username=attrs.get('username')).exists():
            raise ValidationError(detail="User with this username already exists!")

        if User.objects.filter(email=attrs.get('email')).exists():
            raise ValidationError(detail="User with this email already exists!")
        
        if User.objects.filter(phone_number=attrs.get('phone_number')).exists():
            raise ValidationError(detail="User with this phone number already exists!")
        
        return super().validate(attrs)
    
    def create(self,validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )

        user.set_password(validated_data['password'])

        user.save()
        return user