# Generated by Django 4.0.4 on 2022-04-28 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_style_style_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_postal_code',
        ),
    ]
