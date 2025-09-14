from django.db import models


CATEGORY_CHOICES = {
    'electronics': 'electronics',
    'clothing': 'clothing',
    'books': 'books',
}


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    category = models.CharField(choices=CATEGORY_CHOICES)

    class Meta:
        ordering = ['category']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
