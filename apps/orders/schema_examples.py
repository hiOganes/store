from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

from apps.orders.serializers import (
    OrderGetSerializer, OrderPostSerializer, OrderPatchSerializer
)
from apps.orders.models import STATUS_CHOICES



orders_tags = ['Orders']
admin_orders_tags = ['AdminOrders']

orders_list_get_schema = {
    'tags': orders_tags,
    'summary': 'This endpoint returns list user orders',
    'responses': {200: OrderGetSerializer},
}

orders_list_post_schema = {
    'tags': orders_tags,
    'summary': 'This endpoint creates a new order',
    'request': OrderPostSerializer,
    'responses': {201: OrderPostSerializer},
}

orders_detail_get_schema = {
    'tags': orders_tags,
    'summary': 'This endpoint returns detail user order',
}

orders_detail_patch_schema = {
    'tags': orders_tags,
    'summary': 'This endpoint change status order',
    'description': f'Select order id and one of these statuses: '
                   f'{list(STATUS_CHOICES.keys())}',
    'responses': {200: OrderPatchSerializer},
    'request': OrderPatchSerializer,
}

admin_orders_list_get_schema = {
    'tags': admin_orders_tags,
    'summary': 'This endpoint returns list users orders for admin user',
    'parameters': [
            OpenApiParameter(
                name="status",
                description="Filter orders by status",
                required=False,
                type=OpenApiTypes.STR,
                enum=STATUS_CHOICES
            ),
            OpenApiParameter(
                name="user_id",
                description="Filter orders by user_id",
                required=False,
                type=OpenApiTypes.INT,
            ),
    ]
}