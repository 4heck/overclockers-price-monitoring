import logging
from decimal import Decimal, InvalidOperation

from celery import shared_task

from ..models import Product
from ..parsers import ProductParser


@shared_task(bind=True, max_retries=3)
def product_task(self, product_id=None):
    """Product task"""
    logger = logging.getLogger(__name__)

    try:
        product = Product.objects.get(id=product_id)

        # set status
        product.status = Product.STATUS_CHOICE_PROGRESS
        product.save()

        # product parser
        product_parser = ProductParser()
        product_link = product.link
        product_root = product_parser.get_selector_root(link=product_link)
        product_dict = product_parser.parse(root=product_root)

        product.uid = product_dict.get('uid', '').strip()
        product.producer = product_dict.get('producer', '').strip()
        product.model = product_dict.get('model', '').strip()

        try:
            product.price = Decimal(product_dict.get('price'))
        except (InvalidOperation, TypeError):
            pass

        try:
            product.retail_price = Decimal(product_dict.get('retail_price'))
        except (InvalidOperation, TypeError):
            pass

        try:
            product.online_price = Decimal(product_dict.get('online_price'))
        except (InvalidOperation, TypeError):
            pass

        try:
            product.special_price = Decimal(product_dict.get('special_price'))
        except (InvalidOperation, TypeError):
            pass

        product.status = Product.STATUS_CHOICE_DONE
        product.save()
    except Product.DoesNotExist as err:
        logger.warning(err)
    except Exception:
        self.retry(countdown=5)
    return True
