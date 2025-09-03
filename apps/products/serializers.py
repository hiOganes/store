from rest_framework import serializers

from apps.products.models import STATUS_CHOICES, Product


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    category = serializers.ChoiceField(choices=STATUS_CHOICES)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance