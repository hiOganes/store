from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_save

from apps.products.models import Product


@receiver(post_save, sender=Product)
def post_save_product(**kwargs):
    cache.clear()