# Generated by Django 5.1.4 on 2025-02-09 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
