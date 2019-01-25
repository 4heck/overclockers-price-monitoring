"""Admin"""

from django.contrib import admin

from .shopkz import ShopkzAdmin

from ..models import (
    Shopkz,
)

admin.site.register(Shopkz, ShopkzAdmin)
