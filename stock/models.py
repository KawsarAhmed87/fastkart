from django.db import models
from product.models import ProductVariant
from account.models import Account
from transaction.models import Transaction

class StockMovement(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    account_name = models.ForeignKey(Account, related_name='account_info', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, related_name='stock_movements', on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=5) # product stock in or out
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.product_variant} - {self.movement_type} - {self.quantity}"

    @property
    def sub_total(self):
        return self.amount * self.quantity

    class Meta:
        ordering = ['-date']



