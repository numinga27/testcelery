# Generated by Django 3.1.10 on 2023-10-24 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0002_auto_20231023_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='current_time',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='stage_start_time',
            field=models.TextField(null=True),
        ),
    ]
