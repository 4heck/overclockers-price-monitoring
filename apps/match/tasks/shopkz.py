from apps.overclockerskz.models import Product as OverclockerskzProduct
from apps.shopkz.models import Product as ShopkzProduct
from celery import shared_task
from django.db.utils import IntegrityError

from ..models import Shopkz


@shared_task(bind=True, max_retries=3)
def shopkz_task(self):
    """Shopkz task"""
    try:
        overclockerskz_products = OverclockerskzProduct.objects.exclude(article__isnull=True).exclude(article__exact='')

        for overclockerskz_product in overclockerskz_products:
            obj, _ = Shopkz.objects.update_or_create(overclockerskz=overclockerskz_product)
            if not obj.shopkz:
                article = overclockerskz_product.article
                shopkz_product = ShopkzProduct.objects.filter(uid=article).first()
                try:
                    if shopkz_product:
                        obj.shopkz = shopkz_product
                        obj.save()
                    else:
                        shopkz_product = ShopkzProduct.objects.filter(model=article).first()
                        obj.shopkz = shopkz_product
                        obj.save()
                except IntegrityError:
                    pass

    except Exception:
        self.retry(countdown=5)
