# Generated by Django 2.1.4 on 2019-01-08 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0004_auto_20190105_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkz',
            name='online_price_diff',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Разница'),
        ),
        migrations.AddField(
            model_name='shopkz',
            name='online_price_diff_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Процент разницы'),
        ),
    ]
