import uuid

from django.db import models

from constants import ACCOUNT_TYPE, BANK_CODES
from users.models import User


# Create your models here.
class Account(models.Model):
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    account_number = models.CharField(unique=True, max_length=255)
    bank_code = models.CharField(max_length=50, choices=BANK_CODES)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE)
    balance = models.BigIntegerField()

    def __str__(self):
        return self.account_number
