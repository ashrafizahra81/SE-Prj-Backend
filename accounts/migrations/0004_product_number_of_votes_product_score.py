# Generated by Django 4.0.3 on 2022-05-27 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_shop_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='number_of_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='score',
            field=models.FloatField(default=0),
        ),
    ]
