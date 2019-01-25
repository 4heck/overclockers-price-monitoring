import json
import logging
from decimal import Decimal, InvalidOperation

from apps.match.tasks import shopkz_task
from conf import settings
from django import views
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from ..models import Product


class ProductImportView(views.View):
    """Product Import View"""

    logger = logging.getLogger(__name__)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """Dispatch method"""
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """Get"""
        # authorization
        request_access_token = request.GET.get('access_token', '')
        settings_access_token = settings.ACCESS_TOKEN

        if request_access_token != settings_access_token:
            self.logger.warning(f'Unauthorized: {request_access_token} != {settings_access_token}')
            return HttpResponse('Unauthorized', status=401)

        try:
            products = json.loads(request.body)
            if isinstance(products, list):
                # set all products as not available
                Product.objects.all().update(is_available=False)

                # update product's records if exists else create new records
                for product in products:
                    guid = product.get('guid', '').strip()[:255]
                    if guid:
                        name = product.get('name', '').strip()[:255]
                        article = product.get('article', '').strip()[:255]

                        try:
                            purchase_price = Decimal(product.get('purchase_price'))
                        except (InvalidOperation, TypeError):
                            purchase_price = None

                        try:
                            retail_price = Decimal(product.get('retail_price'))
                        except (InvalidOperation, TypeError):
                            retail_price = None

                        try:
                            special_price = Decimal(product.get('special_price'))
                        except (InvalidOperation, TypeError):
                            special_price = None

                        try:
                            online_price = Decimal(product.get('online_price'))
                        except (InvalidOperation, TypeError):
                            online_price = None

                        Product.objects.update_or_create(guid=guid,
                                                         defaults={
                                                             'name': name,
                                                             'article': article,
                                                             'purchase_price': purchase_price,
                                                             'retail_price': retail_price,
                                                             'special_price': special_price,
                                                             'online_price': online_price,
                                                             'is_available': True,
                                                         })

                # run linking process
                shopkz_task.delay()
        except Exception as err:
            self.logger.warning(err)
            return HttpResponse('Internal Error', status=500)
        return HttpResponse('Ok')
