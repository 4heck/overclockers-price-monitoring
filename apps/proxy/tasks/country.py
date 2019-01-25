from celery import shared_task

from ..models import Country
from ..tasks import proxy_task


@shared_task
def country_periodic_task():
    """Country periodic task"""
    countries = Country.objects.all()

    for country in countries:
        proxy_task.delay(country_id=country.id)
