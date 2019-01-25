from django.contrib import admin


class ProductAdmin(admin.ModelAdmin):
    """Product Admin"""

    list_display = ('id', 'guid', 'article', 'name', 'is_available', 'updated_at', 'retail_price', 'online_price',)
    list_filter = ('is_available',)
    list_per_page = 20
    search_fields = ('article', 'name',)
    readonly_fields = ('created_at', 'updated_at',)
