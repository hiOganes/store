from django.db import models

from apps.products.models import Product
from apps.accounts.models import User


STATUS_CHOICES = {
    'pending': 'pending',
    'processing': 'processing',
    'shipped': 'shipped',
    'delivered': 'delivered',
    'cancelled': 'cancelled',
}


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    status = models.CharField(
        choices=STATUS_CHOICES, default=STATUS_CHOICES['pending']
    )
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_purchace = models.DecimalField(max_digits=12, decimal_places=2)