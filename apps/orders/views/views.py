from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.orders.models import Order
from apps.orders import schema_examples
from apps.orders.tasks import get_order_report, external_api_simulation
from apps.orders.serializers import (
    OrderGetSerializer,
    OrderPostSerializer,
    OrderPatchSerializer
)


class OrderListAPIView(APIView):
    model = Order
    permission_classes = [IsAuthenticated]

    @extend_schema(**schema_examples.orders_list_get_schema)
    def get(self, request, *args, **kwargs):
        orders = self.model.objects.filter(user_id=request.user.id)
        serializer = OrderGetSerializer(orders, many=True)
        return Response(data=serializer.data)

    @extend_schema(**schema_examples.orders_list_post_schema)
    def post(self, request, *args, **kwargs):
        serializer = OrderPostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            products_ids = []

            for product in serializer.validated_data['products']:
                print(product.id)
                products_ids.append(product.id)

            get_order_report.delay(products_ids)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class OrderDetailAPIView(APIView):
    model = Order
    serializer_class = OrderGetSerializer
    permission_classes = [IsAuthenticated]

    def check_perimssion(self, request, order):
        return request.user.id == order.user_id or request.user.is_staff

    @extend_schema(**schema_examples.orders_detail_get_schema)
    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(self.model, pk=pk)
        if not self.check_perimssion(request, order):
            return Response(
                data='Access denied', status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.serializer_class(order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(**schema_examples.orders_detail_patch_schema)
    def patch(self, request, pk, *args, **kwargs):
        order = get_object_or_404(self.model, pk=pk)
        if not self.check_perimssion(request, order):
            return Response(
                data='Access denied', status=status.HTTP_403_FORBIDDEN
            )
        serializer = OrderPatchSerializer(
            order, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            if serializer.validated_data['status'] == 'shipped':
                external_api_simulation.delay()
            return Response(
                data=serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )