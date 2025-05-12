from rest_framework import serializers
from .models import Order, OrderItem
from menu.models import MenuItem

class OrderItemSerializer(serializers.ModelSerializer):
    # Serializer for an individual item in an order
    menu_item_name = serializers.CharField(source="menu_item.name", read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'quantity', 'total_price']

    
class OrderCreateSerializer(serializers.ModelSerializer):
    # Serializer for creating order
    items = serializers.ListField(child=serializers.DictField(), write_only=True)
    order_status = serializers.HiddenField(default="PENDING")

    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'items', 'order_status', 'created_at']

    def create(self, validated_data):

        items_data = validated_data.pop('items') # Get entered MenuItem and Quantity in items_data variable
        order = Order.objects.create(**validated_data) # Get validated data in order variable

        order_items = []
        # Iterate each item in item_data and append it
        for item_data in items_data:

            menu_item = MenuItem.objects.get(id=item_data['menu_item']) # Get each Menu id from MenuItem model
            quantity = item_data.get('quantity', 1) # Get customer entered quantity

            order_items.append(OrderItem(order=order, menu_item=menu_item, quantity=quantity))
        
        OrderItem.objects.bulk_create(order_items)
        return order

class OrderDetailSerializer(serializers.ModelSerializer):
    # Serializer for Retrieving order
    customer_name = serializers.CharField(source="customer.username", read_only=True)
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    items = OrderItemSerializer(source="order_items", many=True, read_only=True) # Nested Serializer 
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'restaurant_name', 'items', 'order_status', 'total_price', 'created_at']

class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','order_status']