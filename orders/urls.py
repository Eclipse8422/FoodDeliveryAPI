from django.urls import path
from . import views

urlpatterns= [
    path('', views.OrderCreateListView.as_view(),name="order_create_list"),
    path('<int:order_id>/', views.OrderRetrieveUpdateDeleteView.as_view(),name="order_retrieve_update_delete"),
    path('update-status/<int:order_id>/', views.UpdateOrderStatusView.as_view(),name="update_status"),
    path('user/<int:user_id>/orders/', views.UserOrderView.as_view(),name="user_orders"),
    path('user/<int:user_id>/order/<int:order_id>/', views.UserSpecificOrderView.as_view(),name="user_specific_order"),
]