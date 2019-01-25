from celery import shared_task

from ..models import Category
from ..tasks import category_task


@shared_task
def categories_periodic_task():
    """Categories periodic task"""
    categories = Category.objects.exclude(status=Category.STATUS_CHOICE_PROGRESS)

    for category in categories:
        category_task.delay(category_id=category.id)

    return len(categories)
