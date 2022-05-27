<<<<<<< HEAD
# Generated by Django 4.0.3 on 2022-05-24 18:58
=======
# Generated by Django 4.0.3 on 2022-05-26 12:52
>>>>>>> main

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=100)),
                ('user_phone_number', models.CharField(max_length=20, null=True)),
                ('user_postal_code', models.CharField(max_length=20, null=True)),
                ('user_address', models.CharField(max_length=20, null=True)),
                ('shop_name', models.CharField(max_length=1000, null=True)),
                ('shop_address', models.CharField(max_length=2000, null=True)),
                ('shop_phone_number', models.CharField(max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_price', models.BigIntegerField()),
                ('upload', models.FileField(null=True, upload_to='uploads/')),
                ('inventory', models.IntegerField(default=0)),
                ('product_size', models.CharField(max_length=100, null=True)),
                ('product_color', models.CharField(max_length=100, null=True)),
                ('product_height', models.IntegerField(default=0)),
                ('product_design', models.CharField(max_length=100, null=True)),
                ('product_material', models.CharField(max_length=100, null=True)),
                ('product_country', models.CharField(max_length=100, null=True)),
<<<<<<< HEAD
                ('product_off_percent', models.IntegerField(default=0, null=True)),
=======
                ('product_off_percent', models.IntegerField(default=0)),
>>>>>>> main
                ('is_available', models.BooleanField(default=False)),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style_image_url', models.URLField(null=True)),
                ('style_param_1', models.CharField(default='', max_length=100)),
                ('style_param_2', models.CharField(default='', max_length=100)),
                ('style_param_3', models.CharField(default='', max_length=100)),
                ('style_param_4', models.CharField(default='', max_length=100)),
                ('style_param_5', models.CharField(default='', max_length=100)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.product')),
            ],
        ),
        migrations.CreateModel(
            name='UserStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.style')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='not Accepted', max_length=100, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFavoriteProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductAndStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('product_price', models.BigIntegerField(null=True)),
                ('upload', models.FileField(null=True, upload_to='uploads/')),
                ('product_size', models.CharField(max_length=100, null=True)),
                ('product_height', models.IntegerField(default=0)),
                ('product_design', models.CharField(max_length=100, null=True)),
                ('product_material', models.CharField(max_length=100, null=True)),
                ('product_country', models.CharField(max_length=100, null=True)),
                ('product_off_percent', models.IntegerField(default=0, null=True)),
                ('inventory', models.IntegerField(default=0, null=True)),
                ('style_param_1', models.CharField(default='', max_length=100)),
                ('style_param_2', models.CharField(default='', max_length=100)),
                ('style_param_3', models.CharField(default='', max_length=100)),
                ('style_param_4', models.CharField(default='', max_length=100)),
                ('style_param_5', models.CharField(default='', max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.product')),
                ('shop_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='products1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.IntegerField()),
                ('status', models.CharField(max_length=100)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('complete_date', models.DateTimeField(null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='accounts.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
