from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class DeliveryAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="delivery_agent")
    pincode = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.user.role != "delivery_agent":
            raise ValueError("Only users with role 'delivery_agent' can be registered as delivery agents.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Agent {self.user.username} - {'Available' if self.is_available else 'busy'}"