import random
import string
from django.db import models

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=12, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_transaction_id():
        while True:
            transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            if not Transaction.objects.filter(transaction_id=transaction_id).exists():
                return transaction_id

    def __str__(self):
        return self.transaction_id
