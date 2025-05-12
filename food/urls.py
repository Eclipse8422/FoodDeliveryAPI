
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('menu/', include('menu.urls')),
    path('orders/', include('orders.urls')),

    # JWT djoser
    path('auth/', include('djoser.urls.jwt')),
]
