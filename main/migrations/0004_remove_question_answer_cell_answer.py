# Generated by Django 4.2.3 on 2023-07-25 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_field_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answer',
        ),
        migrations.AddField(
            model_name='cell',
            name='answer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.answer'),
        ),
    ]