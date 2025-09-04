from rest_framework import serializers

from apps.products.models import STATUS_CHOICES, Product
from apps.products.serializers import ProductSerializer
from apps.accounts.serializers import UserSerializer
from apps.orders.models import OrderItem, Order


class OrderGetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    products = ProductSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    created_at = serializers.DateTimeField(read_only=True)


class OrderPostSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    products = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all()
    )
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        products = validated_data.pop('products')
        order = Order.objects.create(user=user, **validated_data)
        print(products)
        for product in products:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                price_at_purchace=1,
            )
        return order