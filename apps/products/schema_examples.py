from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

from apps.products.serializers import ProductSerializer
from apps.products.models import CATEGORY_CHOICES


products_tags = ['Products']

product_list_get_schema = {
    'tags': products_tags,
    'summary': 'This endpoint returns lest products',
    'description': '''You can get the full list of products or filter them''',
    'responses': {200: ProductSerializer},
    'parameters': [
        OpenApiParameter(
            name="category",
            description="Filter products by category",
            required=False,
            type=OpenApiTypes.STR,
            enum=CATEGORY_CHOICES
        ),
        OpenApiParameter(
            name="min_price",
            description="Filter products by current price",
            required=False,
            type=OpenApiTypes.DECIMAL,
        ),
        OpenApiParameter(
            name="max_price",
            description="Filter products by current price",
            required=False,
            type=OpenApiTypes.DECIMAL,
        ),
    ]
}


product_list_post_schema = {
    'tags': products_tags,
    'summary': 'This endpoint creates a new product',
    'description': f'Select category: '
                   f'{list(CATEGORY_CHOICES.keys())}',
    'responses': {201: ProductSerializer},
}


product_detail_get_schema = {
    'tags': products_tags,
    'summary': 'This endpoint returs detial iformation about product',
    'description': '''If you provide the correct data, you can get full 
        infarmation about product.''',
}


product_detail_put_schema = {
    'tags': products_tags,
    'summary': 'This endpoint change product data',
    'description': '''If you provide correct data, you will be able to 
        change the product data.''',
}


product_detail_patch_schema = {
    'tags': products_tags,
    'summary': 'This endpoint partially change product data',
    'description': '''If you provide correct data, you will be able to 
        partially change the product data.''',
}


product_detail_delete_schema = {
    'tags': products_tags,
    'summary': 'This endpoint remove the product',
    'description': '''If you provide correct data, you will be able to 
        delete the product.''',
}