# Generated by Django 5.2 on 2025-05-19 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventmain', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
