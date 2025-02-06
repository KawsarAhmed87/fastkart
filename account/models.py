from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name

class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    reference = models.CharField(max_length=12, blank=True, null=True)  # e.g., Purchase ID / Sale ID / Adjustment ID

    def __str__(self):
        return f"Transaction {self.id} - {self.description}"

class TransactionEntry(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='entries')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    entry_type = models.CharField(max_length=6) # debit or credit

    def __str__(self):
        return f"{self.entry_type} of {self.amount} to {self.account.name}"
