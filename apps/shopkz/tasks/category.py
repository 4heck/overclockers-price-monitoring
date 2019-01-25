import logging

from celery import shared_task
from furl import furl

from ..models import Category, Product
from ..parsers import CategoryParser
from ..tasks import products_task


@shared_task(bind=True, max_retries=3)
def category_task(self, category_id=None):
    """Category task"""
    logger = logging.getLogger(__name__)

    try:
        category = Category.objects.get(id=category_id)

        # set status
        category.status = Category.STATUS_CHOICE_PROGRESS
        category.save()

        # category parser
        category_parser = CategoryParser()
        category_link = category.link
        category_root = category_parser.get_selector_root(link=category_link)
        category_dict = category_parser.parse(root=category_root)

        last_page_number = category_dict.get('last_page_number', 1) + 1
        products = category_dict.get('products', [])

        for page_number in range(2, last_page_number):
            page_link = furl(category_link).add({'PAGEN_1': page_number}).url
            category_root = category_parser.get_selector_root(link=page_link)
            category_dict = category_parser.parse(root=category_root)

            products.extend(category_dict.get('products', []))

        for product in products:
            name = product.get('name')
            link = product.get('link')
            if name and link:
                Product.objects.get_or_create(link=link, category=category, defaults={'name': name})

        category.status = Category.STATUS_CHOICE_DONE
        category.save()
        products_task.delay(category_id=category.id)
    except Category.DoesNotExist as err:
        logger.warning(err)
    except Exception:
        self.retry(countdown=5)
    return True
