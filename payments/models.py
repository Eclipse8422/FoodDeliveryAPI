from django.db import models
from orders.models import Order
# Create your models here.

class Payment(models.Model):

    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    PAYMENT_MODES = [
        ("ONLINE", "Online"),
        ("COD", "Cash on Delivery"),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=10, default="INR")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODES, default="ONLINE")
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    
    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.status}"