from django.db import models


class Country(models.Model):
    """Country model"""

    STATUS_CHOICE_NEW = 0
    STATUS_CHOICE_PROGRESS = 1
    STATUS_CHOICE_DONE = 2
    STATUS_CHOICE_ERROR = 3

    STATUS_CHOICES = (
        (STATUS_CHOICE_NEW, 'Новый'),
        (STATUS_CHOICE_PROGRESS, 'В обработке'),
        (STATUS_CHOICE_DONE, 'Закончен'),
        (STATUS_CHOICE_ERROR, 'Ошибка')
    )
    status = models.PositiveIntegerField(verbose_name='Статус', choices=STATUS_CHOICES, default=STATUS_CHOICE_NEW)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    name = models.CharField(verbose_name='Название', max_length=255)
    link = models.CharField(verbose_name='Ссылка для сбора', max_length=255)

    class Meta:
        """Meta"""

        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return f"{self.name}"
