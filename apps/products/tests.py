from copy import deepcopy

from django.urls import reverse
from rest_framework.test import (
    APIRequestFactory, force_authenticate, APITestCase
)
from rest_framework import status
from django.core.cache import cache

from apps.accounts.models import User
from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from apps.products.views import ProductDetailAPIView, ProductListAPIView
from apps.common.data_tests import (
    test_user_register,
    test_admin_user_register,
    test_products,
    test_products2,
)


class TestProductListAPIView(APITestCase):
    def setUp(self):
        self.url = reverse('products:list')
        self.factory = APIRequestFactory()
        self.view = ProductListAPIView.as_view()
        self.user = User.objects.create_user(**test_user_register)
        self.admin = User.objects.create_user(**test_admin_user_register)
        self.product = Product.objects.create(**test_products)
        self.products = Product.objects.all()

    def test_get_products_authenticated_user(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        serializer = ProductSerializer(self.products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_products_authenticated_admin(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.admin)
        response = self.view(request)
        serializer = ProductSerializer(self.products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_products_unauthenticated(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_products_cahed_hit(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.admin)
        response = self.view(request)
        self.assertIsNotNone(cache.get(request.get_full_path()))
        with self.assertNumQueries(0):
            response = self.view(request)

    def test_get_products_cahed_miss(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.admin)
        cached_data = cache.get(self.url)
        self.assertIsNone(cached_data)
        with self.assertNumQueries(1):
            response = self.view(request)


    def test_post_products_valid_data(self):
        other_product = {
            'name': 'Test2',
            'description': 'Test two',
            'price': 2,
            'stock': 10,
            'category': 'books'
        }
        request = self.factory.post(self.url, other_product, format='json')
        force_authenticate(request, user=self.admin)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Product.objects.filter(name=test_products['name']).exists()
        )

    def test_post_products_invalid_data(self):
        invalid_data = {
            'name': 'Test_invalid_data',
            'description': 'Test_invalid_data',
            'price': 'one',
            'stock': 'five',
            'category': 'invalid_category'
        }
        request = self.factory.post(self.url, invalid_data, format='json')
        force_authenticate(request, user=self.admin)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestProductDetailAPIView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProductDetailAPIView.as_view()
        self.user = User.objects.create_user(**test_user_register)
        self.admin = User.objects.create_user(**test_admin_user_register)
        self.product = Product.objects.create(**test_products)
        self.product2 = Product.objects.create(**test_products2)
        self.products = Product.objects.all()


    def test_get_product_authenticated_user(self):
        request = self.factory.get(
            reverse('products:detail', kwargs={'pk': self.product.pk})
        )
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.product.pk)
        serializer = ProductSerializer(self.product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_authenticated_admin(self):
        request = self.factory.get(
            reverse('products:detail', kwargs={'pk': self.product.pk})
        )
        force_authenticate(request, user=self.admin)
        response = self.view(request, pk=self.product.pk)
        serializer = ProductSerializer(self.product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_unauthenticated(self):
        request = self.factory.get(
            reverse('products:detail', kwargs={'pk': self.product.pk})
        )
        response = self.view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_product_valid_data(self):
        data = deepcopy(test_products)
        data['name'] = 'New name'
        request = self.factory.put(
            reverse('products:detail', kwargs={'pk': self.product.pk}),
            data,
            format='json'
        )
        force_authenticate(request, user=self.admin)
        response = self.view(request, pk=self.product.pk)
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product.name, data['name'])

    def test_put_product_invalid_data(self):
        data = deepcopy(test_products)
        data['stock'] = 0
        request = self.factory.put(
            reverse('products:detail', kwargs={'pk': self.product.pk}),
            data,
            format='json'
        )
        force_authenticate(request, user=self.admin)
        response = self.view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_product_unauthenticated(self):
        data = deepcopy(test_products)
        data['name'] = 'New name'
        request = self.factory.put(
            reverse('products:detail', kwargs={'pk': self.product.pk}),
            data,
            format='json'
        )
        response = self.view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_product_authenticated_user(self):
        data = deepcopy(test_products)
        data['name'] = 'New name'
        request = self.factory.put(
            reverse('products:detail', kwargs={'pk': self.product.pk}),
            data,
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_product_valid_data(self):
        data = {
            "name": "Test2"
        }
        request = self.factory.patch(
            reverse('products:detail', kwargs={'pk': self.product.pk}),
            data,
            format='json'
        )
        force_authenticate(request, user=self.admin)
        response = self.view(request, pk=self.product.pk)
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product.name, data['name'])

    def test_patch_product_invalid_data(self):
        data = {
            "stock": 0
        }
        request = self.factory.patch(
            reverse('products:detail', kwargs={'pk': self.product.pk}),
            data,
            format='json'
        )
        force_authenticate(request, user=self.admin)
        response = self.view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_product_unauthenticated(self):
        data = {
            "name": "Test2"
        }
        request = self.factory.patch(
            reverse('products:detail', kwargs={'pk': self.product.pk}),
            data,
            format='json'
        )
        response = self.view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_product_authenticated_user(self):
        data = {
            "name": "Test2"
        }
        request = self.factory.patch(
            reverse('products:detail', kwargs={'pk': self.product.pk}),
            data,
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_unauthenticated(self):
        amount_before = self.products.count()
        request = self.factory.delete(
            'products:detail', kwargs={'pk': self.product.pk}
        )
        response = self.view(request, pk=self.product.pk)
        amount_after = self.products.count()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(amount_before == amount_after)

    def test_delete_product_user(self):
        amount_before = self.products.count()
        request = self.factory.delete(
            'products:detail', kwargs={'pk': self.product.pk}
        )
        force_authenticate(request, self.user)
        response = self.view(request, pk=self.product.pk)
        amount_after = self.products.count()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(amount_before == amount_after)

    def test_delete_product_admin(self):
        amount_before = self.products.count()
        request = self.factory.delete(
            'products:detail', kwargs={'pk': self.product.pk}
        )
        force_authenticate(request, self.admin)
        response = self.view(request, pk=self.product.pk)
        amount_after = self.products.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(amount_before > amount_after)

    def test_delete_product_invalid_data(self):
        amount_before = self.products.count()
        request = self.factory.delete(
            'products:detail', kwargs={'pk': -1}
        )
        force_authenticate(request, self.admin)
        response = self.view(request, pk=-1)
        amount_after = self.products.count()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(amount_before == amount_after)