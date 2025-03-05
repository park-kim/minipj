# Generated by Django 5.1.6 on 2025-03-05 07:37

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Analysis",
            fields=[
                (
                    "analysis_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "analysis_type",
                    models.CharField(
                        choices=[("SPENDING", "지출"), ("INCOME", "수입")],
                        max_length=50,
                    ),
                ),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("description", models.TextField(blank=True, null=True)),
                ("result_image", models.URLField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "analysis_period",
                    models.CharField(
                        choices=[
                            ("DAILY", "일간"),
                            ("WEEKLY", "주간"),
                            ("MONTHLY", "월간"),
                            ("YEARLY", "연간"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analyses",
                        to="accounts.account",
                    ),
                ),
            ],
        ),
    ]
