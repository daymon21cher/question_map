# Generated by Django 4.2.3 on 2023-07-31 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_question_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='variants',
            field=models.JSONField(default=[], help_text='Варианты ответов'),
        ),
    ]
