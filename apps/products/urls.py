from django.urls import path

from apps.products import views


urlpatterns = [
    path('', views.ProductListAPIView.as_view(), name='product-list'),
    path(
        '<slug:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'
    )
]
