from django.db import models


CATEGORY_CHOICES = {
    'electronics': 'electronics',
    'clothing': 'clothing',
    'books': 'books',
}


class Product(models.Model):
    name = models.CharField()
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=1)
    category = models.CharField(choices=CATEGORY_CHOICES)

    class Meta:
        ordering = ['category']
