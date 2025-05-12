from django.shortcuts import render
from .serializers import RestaurantSerializer
from .models import Restaurant
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied

# Create your views here.
class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_authenticated and user.role == "restaurant_owner":
            return user.restaurants.select_related("owner").filter(owner=user)
        
        return Restaurant.objects.select_related("owner").all()
    
    def perform_create(self, serializer):

        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a restaurant.")
        
        if user.role != "restaurant_owner":
            raise PermissionDenied("Only restaurant owners can create a restaurant.")
        
        serializer.save(owner=user)
