from django.contrib import admin

from ..tasks import product_task


class ProductAdmin(admin.ModelAdmin):
    """Product Admin"""

    def run_parser(self, request, products):
        """Run parser action"""
        for product in products:
            product_task.delay(product_id=product.id)

    run_parser.short_description = "Запустить парсинг"

    actions = (run_parser,)
    list_display = ('id', 'name', 'status', 'updated_at', 'category', 'uid', 'producer', 'model',
                    'retail_price', 'online_price', )
    list_filter = ('status', 'category',)
    search_fields = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at',)
