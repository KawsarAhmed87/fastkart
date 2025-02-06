from django import forms
from .models import Product, ProductVariant

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'short_description', 'description', 'image', 'category', 'brand', 'attribute1', 'attribute2', 'status']
        
    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            if image.size > 2 * 1024 * 1024:  # 2MB limit
                raise forms.ValidationError("Image size must be less than 2MB.")
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Only JPG, JPEG, and PNG images are allowed.")
        return image
    

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product', 'attribute1_value', 'attribute2_value', 'image', 'price']
    
