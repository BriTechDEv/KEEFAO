from django.db import models
from django.core.validators import MinValueValidator
from apps.accounts.models import Member

class Contribution(models.Model):
    class Category(models.TextChoices):
        REGISTRATION = "REGISTRATION", "Alumni Registration"
        MONTHLY = "MONTHLY", "Monthly Contribution"
        WELLWISHER = "WELLWISHER", "Wellwisher/Donation"
        CHALLENGE = "CHALLENGE", "Challenge/Fundraiser"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        VERIFIED = "VERIFIED", "Verified"
        FAILED = "FAILED", "Failed"

    member = models.ForeignKey(
        Member, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="my_contributions"
    )
    contributor_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    amount = models.IntegerField(validators=[MinValueValidator(50)])
    category = models.CharField(
        max_length=20, 
        choices=Category.choices, 
        default=Category.REGISTRATION
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    # REQUIRED: To link back to the M-Pesa/Stripe transaction
    payment_reference = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    message = models.TextField(blank=True)
    
    # Renamed to 'date' to match your Admin 'list_display'
    date = models.DateTimeField(auto_now_add=True) 

    class Meta:
        app_label = 'contributions'
        ordering = ['-date']

    def __str__(self):
        name = self.contributor_name or (self.member.username if self.member else "Anonymous")
        return f"{name} - KES {self.amount}"