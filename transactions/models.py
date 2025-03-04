import uuid

from django.db import models

from accounts.models import Account
from constants import TRANSACTION_METHOD, TRANSACTION_TYPE


# Create your models here.
class TransactionHistory(models.Model):
    transaction_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    account_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.BigIntegerField()
    balance_after_transaction = models.BigIntegerField()
    transaction_description = models.TextField()
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE)
    transaction_method = models.CharField(max_length=50, choices=TRANSACTION_METHOD)
    transaction_date = models.DateTimeField()

    def __str__(self):
        return str(self.transaction_id)
