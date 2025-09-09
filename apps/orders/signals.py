from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.orders.models import Order


@receiver(post_save, sender=Order)
def post_save_product(created, **kwargs):
    if not created:
        cache.clear()