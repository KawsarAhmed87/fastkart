from django.db import models
from transaction.models import Transaction
from supplier.models import Supplier

class Purchase(models.Model):
    date = models.DateField()
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Purchase {self.transaction.transaction_id} - {self.supplier.name}"