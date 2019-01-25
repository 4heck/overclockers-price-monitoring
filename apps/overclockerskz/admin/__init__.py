"""Admin"""

from django.contrib import admin

from .product import ProductAdmin

from ..models import (
    Product,
)

admin.site.register(Product, ProductAdmin)
