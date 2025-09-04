from apps.orders.serializers import OrderGetSerializer, OrderPostSerializer


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