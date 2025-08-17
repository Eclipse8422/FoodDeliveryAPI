from rest_framework import viewsets, status
from .models import Order, OrderItem
from .serializers import (OrderItemSerializer,OrderCreateSerializer,OrderDetailSerializer,UpdateOrderStatusSerializer, MarkOrderDeliveredSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from .permissions import IsRestaurantOwnerOrAdmin, IsDeliveryAgent
from rest_framework.response import Response
from rest_framework.decorators import action

class OrderViewSet(viewsets.ModelViewSet):
    
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        
        if self.action == "create":
            return OrderCreateSerializer
        elif self.action in ["retrieve","list"]:
            return OrderDetailSerializer
        elif self.action in ["update", "partial_update"]:
            return UpdateOrderStatusSerializer
        return OrderDetailSerializer
    
    def get_queryset(self):
        base = Order.objects.select_related("restaurant", "customer").prefetch_related("order_items__menu_item")
        user = self.request.user

        if user.is_staff:
            return base.all()
        
        elif user.role == "restaurant_owner":
            return base.filter(restaurant__owner=user)
        
        elif user.role == "delivery_agent":
            return base.filter(delivery_agent__user=user)
        
        return base.filter(customer=user)


    def perform_create(self, serializer):
        
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to create an order!")
        
        if user.role != "customer":
            raise PermissionDenied("Only customers can create orders!")
        
        serializer.save(customer=user)

    # Implemented because customers can still Update orders using /orders/ endpoint
    def perform_update(self, serializer):
        user = self.request.user

        if user.role not in ["restaurant_owner", "admin"]:
            raise PermissionDenied("You are not allowed to update orders.")

        serializer.save()

    @action(detail=True, methods=["PUT","PATCH"], permission_classes=[IsRestaurantOwnerOrAdmin])
    def update_order_status(self, request, pk=None):

        order = self.get_object()
        
        if order.order_status == "DELIVERED":
            raise ValidationError("You cannot update a delivered order!")
        
        if order.order_status == "CANCELLED":
            raise ValidationError("You cannot update a cancelled order!")
        
        serializer = UpdateOrderStatusSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=True, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        user = self.request.user

        if user != order.customer:
            raise PermissionDenied("You can only cancel your own orders!")
        
        if order.order_status != "PENDING":
            raise PermissionDenied("You can only cancel orders that are still pending!")
        
        order.order_status = "CANCELLED"
        order.save()

        return Response({"message": "Order cancelled successfully."}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["PATCH"], permission_classes=[IsDeliveryAgent])
    def mark_delivered(self, request, pk=None):
        order = self.get_object()
        serializer = MarkOrderDeliveredSerializer(order, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Order marked as delivered"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     