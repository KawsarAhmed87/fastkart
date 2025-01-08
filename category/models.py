from django.db import models
from django.utils.text import slugify
import os

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    image = models.FileField(upload_to='category_images/', null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True) 
    status = models.BooleanField(default=True, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # Check if this is an update to an existing category instance
        if self.pk:
            # Get the original instance from the database
            data = Category.objects.get(pk=self.pk)

            # Check if the image field has changed
            if data.image and data.image != self.image:
                # Delete the old image file
                os.remove(data.image.path)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
