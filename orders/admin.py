from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_status', 'created_at')
    list_filter = ('order_status', 'created_at')
    search_fields = ('customer__username', 'order_status')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'menu_item', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order__customer__username', 'menu_item__name')
