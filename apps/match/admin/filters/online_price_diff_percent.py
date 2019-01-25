from django.contrib import admin


class OnlinePriceDiffPercentFilter(admin.SimpleListFilter):
    """Online Price Diff Filter"""

    title = 'Процент разницы'
    parameter_name = 'is_online_price_diff_percent'

    def lookups(self, request, model_admin):
        """Get lookups"""
        return (
            ('', '-'),
            ('0', 'до -5%'),
            ('1', '(-5) - 0%'),
            ('2', '0 - 5%'),
            ('3', 'от 5%'),
        )

    def queryset(self, request, queryset):
        """Get queryset"""
        value = self.value()
        if value == '0':
            return queryset.filter(online_price_diff_percent__lt=-5)
        elif value == '1':
            return queryset.filter(online_price_diff_percent__gte=-5, online_price_diff_percent__lt=0)
        elif value == '2':
            return queryset.filter(online_price_diff_percent__gte=0, online_price_diff_percent__lt=5)
        elif value == '3':
            return queryset.filter(online_price_diff_percent__gte=5)
        return queryset
