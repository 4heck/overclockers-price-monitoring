from django.contrib import admin


class ProxyAdmin(admin.ModelAdmin):
    """Proxy Admin"""

    list_display = ('id', 'value', 'type', 'is_active', 'updated_at', 'latency',)
    list_filter = ('type', 'is_active', )
    list_per_page = 20
