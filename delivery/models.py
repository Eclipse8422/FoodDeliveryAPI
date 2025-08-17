from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class DeliveryAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="delivery_agent")
    pincode = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Agent {self.user.username} - {'Available' if self.is_available else 'busy'}"