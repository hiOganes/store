from collections import Counter

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
    products = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all()
    )

    def create(self, validated_data):
        user = self.context['request'].user
        products = Counter(validated_data.pop('products'))
        order = Order.objects.create(user=user, **validated_data)
        for product, quantity in products.items():
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchace=1,
            )
            order.total_price += product.price
        order.save()
        return order