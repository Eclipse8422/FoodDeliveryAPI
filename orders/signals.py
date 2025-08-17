from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order

@receiver(post_save, sender=Order)
def AssignAndMarkDeliveryAgents(sender, instance, created, **kwargs):

    # If the order is just created, we skip assignment. Customers create orders with "PENDING" status.
    if created:
        return
     
    # Assign delivery agent when order becomes IN_PROGRESS
    if instance.order_status == "IN_PROGRESS" and not instance.delivery_agent:
        instance.assign_delivery_agent()

    # Mark agent available when order is delivered
    if instance.order_status == "DELIVERED":
        instance.mark_agent_available()
 
    # Change order status from "READY_FOR_PICKUP to "OUT_FOR_DELIVERY"
    if instance.order_status == "READY_FOR_PICKUP" and instance.delivery_agent:
        instance.order_status = "OUT_FOR_DELIVERY"
        instance.save()