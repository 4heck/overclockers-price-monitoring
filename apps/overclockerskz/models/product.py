from django.db import models


class Product(models.Model):
    """Product model"""

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    is_available = models.BooleanField(verbose_name='В наличии', default=True)

    guid = models.CharField(verbose_name='Код 1С', max_length=255, blank=True, null=True)
    name = models.CharField(verbose_name='Наименование', max_length=255, blank=True, null=True)
    article = models.CharField(verbose_name='Артикул', max_length=255, blank=True, null=True)
    purchase_price = models.DecimalField(verbose_name='Закупочная цена', max_digits=12, decimal_places=2,
                                         blank=True, null=True)
    retail_price = models.DecimalField(verbose_name='Розничная цена', max_digits=12, decimal_places=2,
                                       blank=True, null=True)
    special_price = models.DecimalField(verbose_name='Специальная цена', max_digits=12, decimal_places=2,
                                        blank=True, null=True)
    online_price = models.DecimalField(verbose_name='Онлайн цена', max_digits=12, decimal_places=2,
                                       blank=True, null=True)

    class Meta:
        """Meta"""

        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"
