# Generated by Django 4.0.3 on 2022-04-26 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_remove_userquestions_value_question_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_id',
            field=models.IntegerField(default=0),
        ),
    ]