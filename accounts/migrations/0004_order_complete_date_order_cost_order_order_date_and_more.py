# Generated by Django 4.0.4 on 2022-05-13 14:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_product_inventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='complete_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='cost',
            field=models.IntegerField(default=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='COMPLETE', max_length=100),
            preserve_default=False,
        ),
    ]
