import os

import requests
from celery import shared_task
from reportlab.platypus import SimpleDocTemplate, Table
from django.utils import timezone
from django.core.mail import EmailMessage

from apps.products.models import Product


@shared_task
def get_order_report(products_ids):
    table_data = [['Name', 'Description', 'Price', 'Category']]
    for product_id in products_ids:
        product = Product.objects.get(id=product_id)
        table_data.append([
            product.name,
            product.description,
            product.price,
            product.category,
        ])

    path_dir = './apps/orders/orders_reports/'
    file_name = f'Order{timezone.now().timestamp()}.pdf'

    if not os.path.exists(path_dir):
        os.mkdir(path_dir)

    pdf = SimpleDocTemplate(f'{path_dir}{file_name}')
    table = Table(table_data)

    page_elements = []
    page_elements.append(table)

    pdf.build(page_elements)

    simulation_sending_email.delay(path_dir + file_name)

    return f'PDF generated {file_name}'


@shared_task
def simulation_sending_email(path_to_file):
    email = EmailMessage(
        "Hello",
        "Body goes here",
        "from@example.com",
        ["to@example.com"],
    )
    email.attach_file(path_to_file)
    email.send()

    return 'email sending'


@shared_task(max_retries=3)
def external_api_simulation():
    external_url = 'https://jsonplaceholder.typicode.com/'
    response = requests.get(external_url)
    print(response.status_code)
    return 'Success request'