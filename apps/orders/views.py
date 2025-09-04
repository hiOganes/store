from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework import status

from apps.orders.serializers import OrderGetSerializer, OrderPostSerializer
from apps.orders.models import Order, OrderItem
from apps.orders import schema_examples


class OrderListAPIView(APIView):
    model = Order
    permission_classes = [IsAuthenticated]

    @extend_schema(**schema_examples.orders_list_get_schema)
    def get(self, request, *args, **kwargs):
        orders = self.model.objects.filter(user_id=request.user.id)
        print(orders)
        serializer = OrderGetSerializer(orders, many=True)
        return Response(data=serializer.data)

    @extend_schema(**schema_examples.orders_list_post_schema)
    def post(self, request, *args, **kwargs):
        serializer = OrderPostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )