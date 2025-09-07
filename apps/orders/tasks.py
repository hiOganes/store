import os

from celery import shared_task
from reportlab.platypus import SimpleDocTemplate, Table

from apps.products.models import Product


@shared_task
def get_order_report(order):
    table_data = [['Name', 'Description', 'Price', 'Category']]
    products = Product.objects.filter(id__in=order)
    print(order`)
    for product in products:
        table_data.append([
            product.name,
            product.description,
            product.price,
            product.category,
        ])

    if not os.listdir('./orders_reports/'):
        os.mkdir('orders_reports')

    pdf = SimpleDocTemplate(f'Order #{order.id}')
    table = Table(table_data)

    page_elements = []
    page_elements.append(table)

    pdf.build(page_elements)