from django.contrib import admin

from ..tasks import category_task


class CategoryAdmin(admin.ModelAdmin):
    """Category Admin"""

    def run_parser(self, request, categories):
        """Run parser action"""
        for category in categories:
            category_task.delay(category_id=category.id)

    run_parser.short_description = "Запустить парсинг"

    actions = (run_parser,)
    list_display = ('id', 'name', 'status', 'created_at', 'updated_at',)
    list_filter = ('status',)
    search_fields = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at',)
