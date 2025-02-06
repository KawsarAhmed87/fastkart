from django.contrib import admin
from .models import Product, ProductVariant

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'brand', 'status')
    search_fields = ('name', 'sku')
    list_filter = ('status', 'category', 'brand')

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute1_value', 'attribute2_value', 'price')
    search_fields = ('product__name',)