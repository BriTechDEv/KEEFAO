from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

User = settings.AUTH_USER_MODEL


class Payment(models.Model):
    PAYMENT_METHODS = (
        ("mpesa", "M-Pesa"),
        ("stripe", "Stripe"),
    )

    STATUS = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    contributor_name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    amount = models.IntegerField(validators=[MinValueValidator(1)])
    method = models.CharField(max_length=20, choices=[("mpesa", "M-Pesa"), ("stripe", "Stripe")])
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")], default="pending")
    # New Field: Stores info like {"category": "REGISTRATION", "member_id": 5}
    metadata = models.JSONField(default=dict, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'payments'
        indexes = [
            models.Index(fields=["transaction_id"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.contributor_name} - {self.amount} ({self.status})"