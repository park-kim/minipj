import uuid
from datetime import datetime

from django.db import models

from accounts.models import Account
from constants import ANALYSIS_PERIOD, ANALYSIS_TYPE
from users.models import User


class Analysis(models.Model):
    analysis_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="analyses")
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="analyses"
    )
    analysis_type = models.CharField(max_length=50, choices=ANALYSIS_TYPE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    result_image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    analysis_period = models.CharField(max_length=30, choices=ANALYSIS_PERIOD)

    def __str__(self):
        return f"{self.user.username} - {self.analysis_type} ({self.start_date} ~ {self.end_date})"
