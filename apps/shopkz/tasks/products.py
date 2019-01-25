from celery import shared_task

from ..models import Product
from ..tasks import product_task


@shared_task
def products_task(category_id=None):
    """Products periodic task"""
    products = Product.objects.filter(category__pk=category_id).exclude(status=Product.STATUS_CHOICE_PROGRESS)

    for product in products:
        product_task.delay(product_id=product.id)

    return len(products)
