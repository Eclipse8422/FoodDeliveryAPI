from django.urls import path, include
from .views import DeliveryAgentViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register(r"agents", DeliveryAgentViewSet, basename="delivery-agent")

urlpatterns = [
    path("", include(router.urls))
]