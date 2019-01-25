from django.contrib import admin

from ..tasks import proxy_task


class CountryAdmin(admin.ModelAdmin):
    """Country Admin"""

    def run_parser(self, request, countries):
        """Run parser action"""
        for country in countries:
            proxy_task.delay(country_id=country.id)

    run_parser.short_description = "Запустить парсинг"
    actions = (run_parser,)
    list_display = ('id', 'name', 'status', 'created_at', 'updated_at',)
    list_filter = ('status',)
    list_per_page = 20
