"""Admin"""

from django.contrib import admin

from .proxy import ProxyAdmin
from .country import CountryAdmin

from ..models import (
    Proxy,
    Country,
)

admin.site.register(Proxy, ProxyAdmin)
admin.site.register(Country, CountryAdmin)
