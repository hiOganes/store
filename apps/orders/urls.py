from django.urls import path

from apps.orders import views


urlpatterns = [
    path('', views.OrderListAPIView.as_view(), name='orders-list'),
    path('<slug:pk>/', views.OrderDetailAPIView.as_view(), name='orders-detail')
]
