from django.db import models
from product.models import ProductVariant

class StockMovement(models.Model):
    product_variant = models.ForeignKey(ProductVariant, related_name='stock_movements', on_delete=models.CASCADE)
    reference = models.CharField(max_length=12, blank=True, null=True)  # e.g., Purchase ID / Sale ID / Adjustment ID
    movement_type = models.CharField(max_length=5) # product stock in or out
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_variant} - {self.movement_type} - {self.quantity}"

    class Meta:
        ordering = ['-date']



