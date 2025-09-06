from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from apps.products.serializers import ProductSerializer
from apps.products.models import Product
from apps.products import schema_examples
from apps.common.paginations import CustomPagination


class ProductListAPIView(APIView):
    serializer_class = ProductSerializer
    model = Product
    paginations_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly|IsAdminUser]

    @extend_schema(**schema_examples.product_list_get_schema)
    def get(self, request, *args, **kwargs):
        category = request.query_params.get('category', '')
        min_price = request.query_params.get('min_price', 0)
        max_price = request.query_params.get('max_price')
        products = self.model.objects.filter(
            category__icontains=category,
            price__gte=min_price,
        )
        if max_price:
            products = products.filter(price__lte=max_price)
        paginator = self.paginations_class()
        paginated_queryset = paginator.paginate_queryset(products, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(**schema_examples.product_list_post_schema)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            print(product)
            serializer = self.serializer_class(product)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class ProductDetailAPIView(APIView):
    serializer_class = ProductSerializer
    model = Product
    paginations_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly | IsAdminUser]

    @extend_schema(**schema_examples.product_detail_get_schema)
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer_class(product)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(**schema_examples.product_detail_put_schema)
    def put(self, request, pk, *args, **kwargs):
        product = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer_class(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(**schema_examples.product_detail_patch_schema)
    def patch(self, request, pk, *args, **kwargs):
        product = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer_class(
            product, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(**schema_examples.product_detail_delete_schema)
    def delete(self, request, pk, *args, **kwargs):
        product = get_object_or_404(self.model, pk=pk)
        product.delete()
        return Response(
             data={'message': 'Item is deleted'},
             status=status.HTTP_204_NO_CONTENT
         )