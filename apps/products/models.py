from django.db import models


STATUS_CHOICES = {
    'electronics': 'Electronics',
    'clothing': 'Clothing',
    'books': 'Books',
}


class Product(models.Model):
    name = models.CharField()
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(choices=STATUS_CHOICES)
