# Generated by Django 5.1.4 on 2025-02-16 12:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('product', '0002_productvariant_status'),
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_type', models.CharField(max_length=5)),
                ('quantity', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('account_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_info', to='account.account')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_movements', to='product.productvariant')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.transaction')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
