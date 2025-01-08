from django.db import models

class Attribute(models.Model):
    OPTION_CHOICES = [
        ('dropdown', 'Dropdown'),
        ('radio', 'Radio'),
        ('tag', 'Tag')
    ]

    name = models.CharField(max_length=50)
    option = models.CharField(max_length=10, choices=OPTION_CHOICES) 
    status = models.BooleanField(default=True)  
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, related_name="values", on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
