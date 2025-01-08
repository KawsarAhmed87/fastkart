from django.db import models
import os

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.FileField(upload_to='brand_images/', blank=True, null=True)
    status = models.BooleanField(default=True)  # True for active, False for inactive
    created_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Check if this is an update to an existing brand instance
        if self.pk:
            # Get the brand instance from the database
            brand = Brand.objects.get(pk=self.pk)

            # Check if the logo field has changed
            if brand.logo and brand.logo != self.logo:
                # Delete the old logo file
                if os.path.isfile(brand.logo.path):
                    os.remove(brand.logo.path)
                    
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
