from django.urls import path

from apps.orders.views import admin_views


app_name = 'admin-orders'

urlpatterns = [
    path('', admin_views.AdminOrderListAPIView.as_view(), name='list'),
]
