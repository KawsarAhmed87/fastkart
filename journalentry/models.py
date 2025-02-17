from django.db import models
from transaction.models import Transaction
from account.models import Account

class JournalEntry(models.Model):
    date = models.DateField()
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="entries")
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    entry_type = models.CharField(max_length=6)  # 'debit' or 'credit'
    created_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.entry_type} of {self.amount} to {self.account.name}"
