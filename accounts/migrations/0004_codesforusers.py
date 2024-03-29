# Generated by Django 4.1.5 on 2023-05-12 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_random_integer'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodesForUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('code', models.CharField(max_length=1000, null=True)),
                ('created_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
