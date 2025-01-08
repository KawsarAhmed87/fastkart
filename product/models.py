from django.db import models
from attribute.models import Attribute

class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500, blank=True, null=True)
    sku = models.CharField(max_length=12, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    attribute1 = models.ForeignKey(Attribute, related_name='products_with_attribute1', on_delete=models.SET_NULL, blank=True, null=True)
    attribute2 = models.ForeignKey(Attribute, related_name='products_with_attribute2', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)  # True for active, False for inactive

    def __str__(self):
        return self.name
