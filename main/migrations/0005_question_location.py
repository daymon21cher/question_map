# Generated by Django 4.2.3 on 2023-07-26 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_question_answer_cell_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='location',
            field=models.TextField(help_text='Гео локация точки', null=True),
        ),
    ]
