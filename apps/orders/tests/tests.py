from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from rest_framework import status

from apps.orders.models import Order
from apps.accounts.models import User
from apps.products.models import Product
from apps.orders.serializers import OrderGetSerializer
from apps.orders.views.views import OrderListAPIView, OrderDetailAPIView
from apps.common.data_tests import (
    test_user_register,
    test_admin_user_register,
    test_products,
    test_other_user_register
)


class TestOrderListAPIView(APITestCase):
    def setUp(self):
        self.url = reverse('orders:list')
        self.factory = APIRequestFactory()
        self.view = OrderListAPIView.as_view()
        self.user = User.objects.create_user(**test_user_register)
        self.admin = User.objects.create_user(**test_admin_user_register)
        self.product = Product.objects.create(**test_products)
        self.new_order = Order.objects.create(user=self.user)
        self.orders = Order.objects.all()

    def test_get_orders_authenticated(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        serializer = OrderGetSerializer(self.orders, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_orders_unauthenticated(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_order_valid_data(self):
        data = {'products': [self.product.id]}
        request = self.factory.post(self.url, data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.filter(user=self.user).exists())

    def test_post_order_invalid_data(self):
        data = {'products': []}
        request = self.factory.post(self.url, data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestOrderDetailAPIView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = OrderDetailAPIView.as_view()
        self.user = User.objects.create_user(**test_user_register)
        self.admin = User.objects.create_user(**test_admin_user_register)
        self.product = Product.objects.create(**test_products)
        self.new_order = Order.objects.create(user=self.user)
        self.order = Order.objects.get(user_id=self.user.id)

    def test_get_order_authenticated_owner(self):
        request = self.factory.get(
            reverse('orders:detail', kwargs={'pk': self.order.pk})
        )
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.order.pk)
        serializer = OrderGetSerializer(self.order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_order_access_denied(self):
        other_user = User.objects.create_user(**test_other_user_register)
        request = self.factory.get(
            reverse('orders:detail', kwargs={'pk': self.order.pk})
        )
        force_authenticate(request, user=other_user)
        response = self.view(request, pk=self.order.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'Access denied')

    def test_get_order_authenticated_admin(self):
        orders = Order.objects.get(user_id=self.user.id)
        request = self.factory.get(
            reverse('orders:detail', kwargs={'pk': self.order.pk})
        )
        force_authenticate(request, user=self.admin)
        response = self.view(request, pk=self.order.pk)
        serializer = OrderGetSerializer(self.order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_order_unauthenticated(self):
        request = self.factory.get(
            reverse('orders:detail', kwargs={'pk': self.order.pk})
        )
        response = self.view(request, pk=self.order.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_order_valid_status(self):
        data = {'status': 'processing'}
        request = self.factory.patch(
            reverse('orders:detail', kwargs={'pk': self.order.pk}),
            data,
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.order.pk)
        self.order.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.order.status, 'processing')

    def test_patch_order_invalid_status(self):
        data = {'status': 'invalid_status'}
        request = self.factory.patch(
            reverse('orders:detail', kwargs={'pk': self.order.pk}),
            data,
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.order.pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_order_authenticated_other(self):
        other_user = User.objects.create_user(**test_other_user_register)
        data = {'status': 'shipped'}
        request = self.factory.patch(
            reverse('orders:detail', kwargs={'pk': self.order.pk}),
            data,
            format='json'
        )
        force_authenticate(request, user=other_user)
        response = self.view(request, pk=self.order.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'Access denied')