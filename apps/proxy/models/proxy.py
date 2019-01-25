from django.db import models

from .country import Country


class Proxy(models.Model):
    """Proxy model"""

    TYPE_CHOICE_NONE = 0
    TYPE_CHOICE_HTTP = 1
    TYPE_CHOICE_HTTPS = 2
    TYPE_CHOICE_SOCK5 = 3

    TYPE_CHOICES = (
        (TYPE_CHOICE_NONE, 'Неизвестно'),
        (TYPE_CHOICE_HTTP, 'HTTP'),
        (TYPE_CHOICE_HTTPS, 'HTTPS/SSL'),
        (TYPE_CHOICE_SOCK5, 'Sock5')
    )
    type = models.PositiveIntegerField(verbose_name='Тип', choices=TYPE_CHOICES, default=TYPE_CHOICE_NONE)
    is_active = models.BooleanField(verbose_name='Активный', default=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Время последнего запроса', auto_now=True)
    value = models.CharField(verbose_name='Значение', max_length=255)
    latency = models.PositiveIntegerField(verbose_name='Задержка в миллисекундах', null=True, blank=True)
    country = models.ForeignKey(Country, verbose_name='Страна', on_delete=models.CASCADE)

    class Meta:
        """Meta"""

        verbose_name = 'Прокси'
        verbose_name_plural = 'Прокси'
        ordering = ('-latency',)

    def __str__(self):
        return f"{self.value}"
