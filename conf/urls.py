"""Urls"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('shopkz/', include('apps.shopkz.urls')),
    path('overclockerskz/', include('apps.overclockerskz.urls')),
]
