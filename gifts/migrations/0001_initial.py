# Generated by Django 4.1.4 on 2023-05-04 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('discount_code', models.CharField(max_length=20)),
                ('score', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=100)),
                ('date', models.DateField(null=True)),
            ],
        ),
    ]
