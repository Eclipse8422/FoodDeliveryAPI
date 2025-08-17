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

        items_data = validated_data.pop('items') # Get the entered MenuItem and Quantity in items_data variable
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
    delivery_agent = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    razorpay_order_id = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'restaurant_name', 'items', 'order_status',
                'total_price', 'delivery_agent', 'payment_status', 'razorpay_order_id', 'created_at',]

    def get_delivery_agent(self, obj):
        if obj.delivery_agent:
            return{
                "id": obj.delivery_agent.id,
                "name": obj.delivery_agent.user.username,
                "pincode": obj.delivery_agent.pincode
            }   
        return None

    def get_payment_status(self, obj):
        return obj.payment.status if hasattr(obj, 'payment') and obj.payment else None

    def get_razorpay_order_id(self, obj):
        return obj.payment.razorpay_order_id if hasattr(obj, 'payment') and obj.payment else None

class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','order_status']

    def validate(self, attrs):
        order = self.instance
        new_status = attrs.get('order_status')

        # Restaurant Owners cannot change their order_status to IN_PROGRESS unless a payment is done if the payment_mode is ONLINE,
        # For COD skip
        if new_status == "IN_PROGRESS":
            payment = getattr(order, 'payment', None)

            if not payment:
                raise serializers.ValidationError("Payment record missing.")

            if payment.payment_mode == "ONLINE" and payment.status != "success":
                raise serializers.ValidationError("Cannot start order unless online payment is successful.")

        return attrs


class MarkOrderDeliveredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'order_status']

    def validate(self, attrs):
        user = self.context['request'].user
        order = self.instance

        if not order.delivery_agent or order.delivery_agent.user != user:
            raise serializers.ValidationError("You are not assigned to this order.")
        
        if order.order_status != 'OUT_FOR_DELIVERY':
            raise serializers.ValidationError("Order is not out for delivery.")
        
        # agent can only update "DELIVERED" as a status
        if attrs.get("order_status") != "DELIVERED":
            raise serializers.ValidationError("You can only mark this order as DELIVERED.")

        return attrs