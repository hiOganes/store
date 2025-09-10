from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema
from rest_framework import status

from apps.orders.models import Order
from apps.orders import schema_examples
from apps.orders.serializers import OrderGetSerializer


class AdminOrderListAPIView(APIView):
    model = Order
    permission_classes = [IsAdminUser]
    serializer_class = OrderGetSerializer

    @extend_schema(**schema_examples.admin_orders_list_get_schema)
    def get(self, request, *args, **kwargs):
        status_order = request.query_params.get('status_order')
        user_id = request.query_params.get('user_id')
        if user_id:
            orders = self.model.objects.filter(user_id=user_id)
        if status_order:
            orders = self.model.objects.filter(status__iexact=status_order)
        if not user_id and not status_order:
            orders = self.model.objects.all()
        serializer = self.serializer_class(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)