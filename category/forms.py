from django import forms
from .models import Category
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'image', 'status']

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            # Validate file type
            if not image.name.endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError('Only JPG, JPEG, and PNG formats are allowed.')

            # Validate file size (max 2 MB)
            if image.size > 2 * 1024 * 1024:  # 2 MB in bytes
                raise ValidationError('The image file is too large. Size should not exceed 2 MB.')

        return image

    
    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A category with this name already exists.")
        return name
