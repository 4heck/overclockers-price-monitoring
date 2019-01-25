from django.db import models

from .category import Category


class Product(models.Model):
    """Product model"""

    STATUS_CHOICE_NEW = 'NEW'
    STATUS_CHOICE_PROGRESS = 'PROGRESS'
    STATUS_CHOICE_DONE = 'DONE'
    STATUS_CHOICE_ERROR = 'ERROR'

    STATUS_CHOICES = (
        (STATUS_CHOICE_NEW, 'Новый'),
        (STATUS_CHOICE_PROGRESS, 'В обработке'),
        (STATUS_CHOICE_DONE, 'Закончен'),
        (STATUS_CHOICE_ERROR, 'Ошибка')
    )

    status = models.CharField(verbose_name='Статус', max_length=255, choices=STATUS_CHOICES, default=STATUS_CHOICE_NEW)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    link = models.URLField(verbose_name='Ссылка для сбора', max_length=255)
    name = models.CharField(verbose_name='Название', max_length=255)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    uid = models.CharField(verbose_name='UID', max_length=255, null=True, blank=True)
    producer = models.CharField(verbose_name='Производитель', max_length=255, null=True, blank=True)
    price = models.DecimalField(verbose_name='Цена по прайсу', max_digits=12, decimal_places=2,
                                blank=True, null=True)
    retail_price = models.DecimalField(verbose_name='Цена в магазинах сети', max_digits=12, decimal_places=2,
                                       blank=True, null=True)
    online_price = models.DecimalField(verbose_name='Цена в интернет-магазине', max_digits=12, decimal_places=2,
                                       blank=True, null=True)
    special_price = models.DecimalField(verbose_name='Цена товара недели', max_digits=12, decimal_places=2,
                                        blank=True, null=True)
    model = models.CharField(verbose_name='Модель', max_length=255, null=True, blank=True)

    class Meta:
        """Meta"""

        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('category', 'producer', 'model',)

    def __str__(self):
        return f"{self.name}"
