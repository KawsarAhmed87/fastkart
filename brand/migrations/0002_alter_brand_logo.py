# Generated by Django 5.1.1 on 2024-11-05 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to='brand_images/'),
        ),
    ]
