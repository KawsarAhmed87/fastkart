from django.db import models
from attribute.models import Attribute, AttributeValue
from category.models import Category
from brand.models import Brand
class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500, blank=True, null=True)
    sku = models.CharField(max_length=12, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    attribute1 = models.ForeignKey(Attribute, related_name='products_with_attribute1', on_delete=models.SET_NULL, blank=True, null=True)
    attribute2 = models.ForeignKey(Attribute, related_name='products_with_attribute2', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)  # True for active, False for inactive
   
    def __str__(self):
        return self.name
    
    """  def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return 0 """


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    attribute1_value = models.ForeignKey(AttributeValue, related_name='variants_with_attribute1', on_delete=models.SET_NULL, blank=True, null=True)
    attribute2_value = models.ForeignKey(AttributeValue, related_name='variants_with_attribute2', on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        attr1 = self.attribute1_value.value if self.attribute1_value else "N/A"
        attr2 = self.attribute2_value.value if self.attribute2_value else "N/A"
        return f"{self.product.name} - {attr1} - {attr2}"
    
    def current_stock(self):
        """Calculate current stock based on movements"""
        stock_in = self.stock_movements.filter(movement_type='IN').aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        stock_out = self.stock_movements.filter(movement_type='OUT').aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        return stock_in - stock_out  # Returns the current stock without saving to the database



""" 
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # One review per user per product

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating} Stars)" """