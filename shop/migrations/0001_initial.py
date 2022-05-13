# Generated by Django 4.0.4 on 2022-05-09 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=1000)),
                ('shop_description', models.CharField(max_length=5000, null=True)),
                ('shop_address', models.CharField(max_length=2000, null=True)),
                ('shop_phone_num', models.IntegerField(null=True)),
                ('shop_owner_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('description', models.CharField(default='', max_length=50)),
                ('price', models.IntegerField(default=0)),
                ('image', models.URLField(null=True)),
                ('shop_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.shop')),
            ],
        ),
    ]