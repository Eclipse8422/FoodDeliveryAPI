from django.db import models
from restaurants.models import Restaurant
from menu.models import MenuItem
from delivery.models import DeliveryAgent
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    ORDER_STATUS = (
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('OUT_FOR_DELIVERY','Out for Delivery'),
        ('DELIVERED','Delivered'),
        ('CANCELLED','Cancelled'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, through="OrderItem")
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default="PENDING")
    delivery_agent = models.ForeignKey(DeliveryAgent, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def total_price(self):
        return sum(item.total_price() for item in self.order_items.all())
    
    def assign_delivery_agent(self):
        # Auto assign delivery agent based on pincode of the restaurant and the agent
        if self.order_status == "IN_PROGRESS" and not self.delivery_agent:
            available_agent = DeliveryAgent.objects.filter(
                pincode=self.restaurant.pincode, is_available=True
                ).order_by('created_at').first()
            
            if available_agent:
                self.delivery_agent = available_agent
                available_agent.is_available = False # mark agent as busy
                available_agent.save()
                self.save()

    def mark_agent_available(self):
        
        if self.order_status == "DELIVERED" and self.delivery_agent:
            self.delivery_agent.is_available = True # Mark agent as available once order is delivered
            self.delivery_agent.save()


    def __str__(self):
        return f"Order {self.id} by {self.customer.email} - {self.order_status}"


# This calculates quantity of each MenuItem with its price
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return self.menu_item.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in Order {self.order.id}"