from apps.overclockerskz.models import Product as OverclockerskzProduct
from apps.shopkz.models import Product as ShopkzProduct
from django.db import models
from django.dispatch import receiver


class Shopkz(models.Model):
    """Shopkz Model"""

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    overclockerskz = models.OneToOneField(OverclockerskzProduct, verbose_name='Продукт overclockers.kz',
                                          on_delete=models.CASCADE, null=True, blank=True)
    shopkz = models.OneToOneField(ShopkzProduct, verbose_name='Продукт shop.kz', on_delete=models.CASCADE,
                                  null=True, blank=True)
    online_price_diff = models.DecimalField(verbose_name='Разница', max_digits=12, decimal_places=2,
                                            blank=True, null=True)
    online_price_diff_percent = models.DecimalField(verbose_name='Процент разницы', max_digits=12, decimal_places=2,
                                                    blank=True, null=True)

    def get_online_price_diff_method(self):
        """Online price difference"""
        try:
            if self.overclockerskz and self.shopkz:
                return self.shopkz.online_price - self.overclockerskz.online_price
            else:
                return 0
        except (TypeError, ValueError):
            return 0

    get_online_price_diff_method.short_description = 'Разница'

    def get_online_price_diff_percent_method(self):
        """Online price difference in percents"""
        try:
            if self.overclockerskz and self.overclockerskz.online_price:
                return int((self.get_online_price_diff_method() / self.overclockerskz.online_price) * 100)
            else:
                return 0
        except (TypeError, ValueError):
            return 0

    get_online_price_diff_percent_method.short_description = 'Процент разницы'

    class Meta:
        """Meta"""

        verbose_name = 'Продукт shop.kz'
        verbose_name_plural = 'Продукты shop.kz'
        ordering = ('overclockerskz',)

    def __str__(self):
        return f"{self.pk}"


@receiver(models.signals.pre_save, sender=Shopkz)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Delete old files on Image update"""
    if not instance.pk:
        return False

    instance.online_price_diff = instance.get_online_price_diff_method()
    instance.online_price_diff_percent = instance.get_online_price_diff_percent_method()
