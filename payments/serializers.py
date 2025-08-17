from rest_framework import serializers
from .models import Payment
from orders.models import Order
import razorpay
import os

class PaymentSerializer(serializers.ModelSerializer):

    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    payment_mode = serializers.ChoiceField(choices=[('ONLINE', 'Online'), ('COD', 'Cash on Delivery')])

    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'currency', 'status', 'razorpay_order_id', 'payment_mode']
        read_only_fields = ['razorpay_order_id', 'status', 'currency', 'amount']

    def validate_order(self, order):
        
        user = self.context['request'].user

        if user != order.customer:
            raise serializers.ValidationError("You can only pay for your own orders.")

        if order.order_status in ["CANCELLED", "DELIVERED"]:
            raise serializers.ValidationError(f"You cannot pay for a {order.order_status.lower()} order.")
        
        if hasattr(order, 'payment'):
            raise serializers.ValidationError("This order already has a payment.")

        return order

    def create(self, validated_data):
        order = validated_data['order']
        payment_mode = validated_data['payment_mode']
        amount = order.total_price()

        razorpay_order_id = None
        currency = "INR"
        status = "pending"

        if payment_mode == "ONLINE":
            api_key = os.getenv('RAZORPAY_API_KEY')
            api_secret = os.getenv('RAZORPAY_API_SECRET')

            if not api_key or not api_secret:
                raise serializers.ValidationError("Razorpay credentials are not set in environment variables.")
        
            client = razorpay.Client(auth=('api_key','api_secret'))

            razorpay_order = client.order.create({
                "amount": int(amount * 100),  # Razorpay uses Paisa, hence need to * 100
                "currency": currency,
                "payment_capture": 1
            })
            
            razorpay_order_id = razorpay_order["id"]

        elif payment_mode == "COD":
            status = "success"

        payment = Payment.objects.create(
            order=order,
            amount=amount,
            currency=currency,
            razorpay_order_id=razorpay_order_id,
            status=status,
            payment_mode=payment_mode
        )
        
        return payment