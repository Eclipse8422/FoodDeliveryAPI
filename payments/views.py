from django.shortcuts import render
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Customer can see only their own payments
        user = self.request.user
        return Payment.objects.filter(order__customer=user)
    