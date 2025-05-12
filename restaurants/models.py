from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

User=get_user_model()

class Restaurant(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')
    name=models.CharField(max_length=100, unique=True)
    address=models.TextField()
    pincode=models.CharField(max_length=10, null=False)
    phone_number=PhoneNumberField(unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Owned By {self.owner.username}"