"""Admin"""

from django.contrib import admin

from .category import CategoryAdmin
from .product import ProductAdmin

from ..models import (
    Category,
    Product,
)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.site_header = 'Мониторинг цен'
admin.site.site_title = 'Мониторинг цен'
admin.site.index_title = 'Панель управления'
