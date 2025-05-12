from django.shortcuts import render
from .serializers import MenuItemSerializer
from .models import MenuItem
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .permissions import IsMenuOwnerOrReadOnly
from restaurants.models import Restaurant
# Create your views here.

class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.select_related("restaurant").all()
    permission_classes = [IsMenuOwnerOrReadOnly]
    

    def get_queryset(self):
        
        user = self.request.user

        if user.is_authenticated and user.role == "restaurant_owner":
            return MenuItem.objects.select_related("restaurant").filter(restaurant__owner=user)
        
        return MenuItem.objects.select_related("restaurant").all()
    
    def perform_create(self, serializer):
        
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a menu-item.")
    
        if user.role != "restaurant_owner":
            raise PermissionDenied("Only restaurant owners can add menu items.")
        
        # Checking if the current user actually owns the restaurant

        restaurant_id = self.request.data.get('restaurant')

        try:
            restaurant = user.restaurants.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise PermissionDenied("Invalid restaurant or you do not own this restaurant.")

        serializer.save(restaurant=restaurant)

    def perform_update(self, serializer):
        
        user = self.request.user
        instance = serializer.instance
        new_restaurant_id = self.request.data.get("restaurant")

        # Checking if the menu item belongs to the user's restaurant
        if instance.restaurant.owner != user :
            raise PermissionDenied("You can only update your own restaurant's menu items.")
        
        # Prevents restaurant change on update
        if new_restaurant_id and str(instance.restaurant.id) != str(new_restaurant_id):
            raise PermissionDenied("You cannot change the restaurant of a menu item.")
        
        serializer.save()
    
    