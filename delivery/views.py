from django.shortcuts import render
from .models import DeliveryAgent
from .serializers import DeliveryAgentSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsApprovedDeliveryAgent


class DeliveryAgentViewSet(viewsets.ModelViewSet):
    queryset = DeliveryAgent.objects.all()
    serializer_class = DeliveryAgentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return DeliveryAgent.objects.all()
        return DeliveryAgent.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user

        if user.role != "delivery_agent":
            raise PermissionDenied("Only users with role 'delivery_agent' can register.")
        
        serializer.save(user=user)

    def perform_update(self, serializer):
        user = self.request.user

        if user.role != "delivery_agent":
            raise PermissionDenied("Only delivery agents can update their profile.")
        
        serializer.save()
    
    # Only Approved delivery agents can update their profile
    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsApprovedDeliveryAgent()]
        elif self.action == "approve":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["POST"], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        print(f"User: {request.user}, is_staff: {request.user.is_staff}, role: {request.user.role}")
        
        agent = self.get_object()
        if agent.is_approved:
            return Response({"detail": "Agent already approved."}, status=status.HTTP_400_BAD_REQUEST)
        
        agent.is_approved = True
        agent.save()
        return Response({"detail": "Agent approved successfully."}, status=status.HTTP_200_OK)
