from django import forms
from django.core.exceptions import ValidationError
from .models import Brand

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'logo', 'status']

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')

        # Check if an image was uploaded
        if logo:
            # Validate file type
            if not logo.name.endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError('Only JPG, JPEG, and PNG formats are allowed.')

            # Validate file size (max 2 MB)
            if logo.size > 2 * 1024 * 1024:  # 2 MB in bytes
                raise ValidationError('The image file is too large. Size should not exceed 2 MB.')

        return logo
