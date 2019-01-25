import logging
from decimal import Decimal, InvalidOperation

from django import views
from django.http import JsonResponse

from ..models import Product
from ..parsers import ProductParser


class ProductView(views.View):
    """Product View"""

    logger = logging.getLogger(__name__)

    def get(self, request, product_id=None):
        """Get"""
        response = {}

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

            product.uid = product_dict.get('uid')
            product.producer = product_dict.get('producer')
            product.model = product_dict.get('model')

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
            self.logger.warning(err)

        return JsonResponse({'data': response})
