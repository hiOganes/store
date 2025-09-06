from apps.orders.serializers import (
    OrderGetSerializer, OrderPostSerializer, OrderPatchSerializer
)
from apps.orders.models import STATUS_CHOICES


orders_tags = ['Orders']

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