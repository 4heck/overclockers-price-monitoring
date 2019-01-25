from django.contrib import admin
from django.db.models import Q


class IsEmptyMatchFilter(admin.SimpleListFilter):
    """Empty Match Filter"""

    title = 'Есть совпадения'
    parameter_name = 'is_empty_match'

    def lookups(self, request, model_admin):
        """Get lookups"""
        return (
            ('', '-'),
            ('yes', 'Да'),
            ('no', 'Нет'),
        )

    def queryset(self, request, queryset):
        """Get queryset"""
        value = self.value()
        if value == 'yes':
            return queryset.filter(overclockerskz__isnull=False, shopkz__isnull=False)
        elif value == 'no':
            return queryset.filter(Q(overclockerskz__isnull=True) | Q(shopkz__isnull=True))
        return queryset
