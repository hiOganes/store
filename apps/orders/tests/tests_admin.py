from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from rest_framework import status

from apps.orders.models import Order
from apps.accounts.models import User
from apps.orders.serializers import OrderGetSerializer
from apps.orders.views.admin_views import AdminOrderListAPIView
from apps.common.data_tests import (
    test_user_register,
    test_admin_user_register,
)


class TestAdminOrderListAPIView(APITestCase):
    def setUp(self):
        self.url = reverse('admin-orders:list')
        self.factory = APIRequestFactory()
        self.view = AdminOrderListAPIView.as_view()
        self.user = User.objects.create_user(**test_user_register)
        self.admin = User.objects.create_user(**test_admin_user_register)
        self.new_order = Order.objects.create(user=self.user)
        self.orders = Order.objects.all()

    def test_get_orders_admin_authenticated(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.admin)
        response = self.view(request)
        serializer = OrderGetSerializer(self.orders, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orders_user_authenticated(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        serializer = OrderGetSerializer(self.orders, many=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_orders_not_authenticated(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        serializer = OrderGetSerializer(self.orders, many=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)