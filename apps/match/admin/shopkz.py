import csv

from apps.match.tasks import shopkz_task
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.utils.html import mark_safe

from .filters import IsEmptyMatchFilter, OnlinePriceDiffPercentFilter


class ShopkzAdmin(admin.ModelAdmin):
    """Shopkz Admin"""

    def product_overclockerskz(self, obj):
        """Product overclockers.kz"""
        if obj.overclockerskz:
            return mark_safe('<span title="{title}">{value}</span>'.format(title=obj.overclockerskz.name,
                                                                           value=obj.overclockerskz.name[:50]))

    product_overclockerskz.short_description = 'Продукт overclockers.kz'
    product_overclockerskz.allow_tags = True

    def product_shopkz(self, obj):
        """Product shop.kz"""
        if obj.shopkz:
            return mark_safe('<span title="{title}">{value}</span>'.format(title=obj.shopkz.name,
                                                                           value=obj.shopkz.name[:50]))

    product_shopkz.short_description = 'Продукт shop.kz'
    product_shopkz.allow_tags = True

    def online_price_diff_color(self, obj):
        """Get online price diff"""
        online_price_diff_percent = obj.online_price_diff_percent
        color = 'black'
        if online_price_diff_percent >= 5:
            color = 'green'
        elif online_price_diff_percent <= -5:
            color = 'red'
        return mark_safe('<div style="background: {color}; width: 28px; height: 28px;'
                         'border-radius: 14px;"></div>'.format(color=color))

    online_price_diff_color.allow_tags = True
    online_price_diff_color.short_description = 'Светофор'

    def overclockerskz_online_price(self, obj):
        """Get online price"""
        if obj.overclockerskz and obj.overclockerskz.online_price:
            return obj.overclockerskz.online_price

    overclockerskz_online_price.short_description = 'Онлайн цена overclockers.kz'

    def shopkz_online_price(self, obj):
        """Get online price"""
        if obj.shopkz and obj.shopkz.online_price:
            return obj.shopkz.online_price

    shopkz_online_price.short_description = 'Цена shop.kz'

    def export_as_csv(self, request, matches):
        """Export csv file"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=output.csv'
        csv_writer = csv.writer(response, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

        # заголовок
        col_names = [
            '<overclockers.kz>',
            'Код 1С',
            'Наименование',
            'Артикул',
            'Закупочная цена',
            'Специальная цена',
            'Розничная цена',
            '<Разница>',
            'Онлайн цена',
            'Цена в ИМ (shop.kz)',
            'Разница (Цена)',
            'Разница (Процент)',
            '<shop.kz>',
            'Ссылка для сбора',
            'Название',
            'Категория',
            'UID',
            'Производитель',
            'Цена по прайсу',
            'Цена в магазинах сети',
            'Цена товара недели',
            'Модель',
        ]

        csv_writer.writerow([item.encode('utf8').decode('utf8') for item in col_names])

        for match in matches:
            # overclockers.kz
            guid = match.overclockerskz.guid if match.overclockerskz else ''
            name = match.overclockerskz.name if match.overclockerskz else ''
            article = match.overclockerskz.article if match.overclockerskz else ''
            purchase_price = match.overclockerskz.purchase_price if match.overclockerskz else ''
            retail_price = match.overclockerskz.retail_price if match.overclockerskz else ''
            special_price = match.overclockerskz.special_price if match.overclockerskz else ''
            online_price = match.overclockerskz.online_price if match.overclockerskz else ''

            # shop.kz
            shopkz_link = match.shopkz.link if match.shopkz else ''
            shopkz_name = match.shopkz.name if match.shopkz else ''
            shopkz_category = match.shopkz.category if match.shopkz else ''
            shopkz_uid = match.shopkz.uid if match.shopkz else ''
            shopkz_producer = match.shopkz.producer if match.shopkz else ''
            shopkz_price = match.shopkz.price if match.shopkz else ''
            shopkz_retail_price = match.shopkz.retail_price if match.shopkz else ''
            shopkz_online_price = match.shopkz.online_price if match.shopkz else ''
            shopkz_special_price = match.shopkz.special_price if match.shopkz else ''
            shopkz_model = match.shopkz.model if match.shopkz else ''

            # differences
            online_price_diff = match.online_price_diff or ''
            online_price_diff_percent = match.online_price_diff_percent or ''

            items = [
                '',
                guid,
                name,
                article,
                purchase_price,
                special_price,
                retail_price,
                '',
                online_price,
                shopkz_online_price,
                online_price_diff,
                online_price_diff_percent,
                '',
                shopkz_link,
                shopkz_name,
                shopkz_category,
                shopkz_uid,
                shopkz_producer,
                shopkz_price,
                shopkz_retail_price,
                shopkz_special_price,
                shopkz_model,
            ]
            csv_writer.writerow([str(item).encode('utf8').decode('utf8') for item in items])

        return response

    export_as_csv.short_description = "Выгрузить в csv"

    def link_products(self, request):
        """Link products"""
        shopkz_task.delay()  # if it will freeze, call delay method
        return HttpResponseRedirect("../")

    def get_urls(self):
        """Get url"""
        urls = super().get_urls()
        my_urls = [
            path('link_products/', self.link_products),
        ]
        return my_urls + urls

    actions = (export_as_csv,)
    list_filter = (IsEmptyMatchFilter, 'overclockerskz__is_available',
                   OnlinePriceDiffPercentFilter, 'shopkz__category',)
    list_display = ('id', 'product_overclockerskz', 'product_shopkz',
                    'overclockerskz_online_price', 'shopkz_online_price',
                    'online_price_diff', 'online_price_diff_percent', 'online_price_diff_color',)
    search_fields = ('overclockerskz__name', 'shopkz__name',)
    list_select_related = ('overclockerskz', 'shopkz',)
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at',)
    raw_id_fields = ('overclockerskz', 'shopkz',)
    change_list_template = "entities/product_changelist.html"
