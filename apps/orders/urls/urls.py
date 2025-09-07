from django.urls import path

from apps.orders.views import views


app_name = 'orders'

urlpatterns = [
    path('', views.OrderListAPIView.as_view(), name='list'),
    path('<slug:pk>/', views.OrderDetailAPIView.as_view(), name='detail')
]
