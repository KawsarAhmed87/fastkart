from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'short_description', 'sku', 'description', 'image', 'attribute1', 'attribute2']
