from django.shortcuts import render,get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import OrderCreationSerializer, OrderDetailSerializer, UpdateOrderStatusSerializer
from .models import Order
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from django.contrib.auth import get_user_model

User=get_user_model()

    
class OrderCreateListView(GenericAPIView):
    serializer_class=OrderCreationSerializer
    queryset=Order.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request):

        orders = self.get_queryset()
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        user = request.user

        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderRetrieveUpdateDeleteView(GenericAPIView):
    serializer_class=OrderDetailSerializer
    permission_classes=[IsAdminUser]

    def get(self,request,order_id):
        order=get_object_or_404(Order, pk=order_id)

        serializer=self.serializer_class(instance=order)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,order_id):
        order=get_object_or_404(Order, pk=order_id)

        serializer=self.serializer_class(instance=order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,order_id):
        order=get_object_or_404(Order, pk=order_id)

        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UpdateOrderStatusView(GenericAPIView):
    serializer_class=UpdateOrderStatusSerializer
    permission_classes=[IsAuthenticated,IsAdminUser]

    def put(self,request,order_id):
        order=get_object_or_404(Order, pk=order_id)

        serializer=self.serializer_class(data=request.data, instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserOrderView(GenericAPIView):
    serializer_class=OrderDetailSerializer
    permission_classes=[IsAuthenticated,IsAdminUser]

    def get(self,request,user_id):
        user=get_object_or_404(User, pk=user_id)

        orders=Order.objects.all().filter(customer=user)

        serializer=self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    

class UserSpecificOrderView(GenericAPIView):
    serializer_class=OrderDetailSerializer
    permission_classes=[IsAuthenticated,IsAdminUser]

    def get(self,request,user_id,order_id):
        user=get_object_or_404(User, pk=user_id)

        order=get_object_or_404(Order, customer=user, pk=order_id)

        serializer=self.serializer_class(instance=order)
        return Response(data=serializer.data,status=status.HTTP_200_OK)