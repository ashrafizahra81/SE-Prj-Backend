# Generated by Django 4.0.3 on 2022-04-26 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_remove_question_question_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquestions',
            name='value',
            field=models.FloatField(default=0),
        ),
    ]
