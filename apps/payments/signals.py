from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from .models import Payment
import logging

logger = logging.getLogger("payments")

@receiver(post_save, sender=Payment)
def handle_payment_success(sender, instance, created, **kwargs):
    """
    Automatically creates a Contribution record when a Payment is marked as 'completed'.
    """
    if instance.status == "completed":
        # LOCAL IMPORTS to prevent Circular Import Errors
        from apps.contributions.models import Contribution
        # Ensure this matches your ACTUAL model name in apps/accounts/models.py
        from apps.accounts.models import Member 

        # 1. Idempotency Check
        if not Contribution.objects.filter(payment_reference=instance.transaction_id).exists():
            try:
                # 2. Get category from metadata
                category = instance.metadata.get("category", "MONTHLY")

                # 3. Create the Contribution record
                Contribution.objects.create(
                    member=instance.user,
                    contributor_name=instance.contributor_name,
                    phone=instance.phone,
                    email=instance.email,
                    amount=instance.amount,
                    # We store the transaction_id as the payment_reference
                    payment_reference=instance.transaction_id, 
                    category=category,
                    status="VERIFIED", # Match the Status choices in your Contribution model
                )

                # 4. Update Member Balance (Thread-Safe)
                if instance.user:
                    # Note: Ensure 'total_contributed' exists on your Member model
                    # If it doesn't exist, remove this block to avoid 500 errors.
                    Member.objects.filter(id=instance.user.id).update(
                        total_contributed=F('total_contributed') + instance.amount
                    )

                logger.info(f"Successfully processed contribution for {instance.transaction_id}")

            except Exception as e:
                logger.error(f"Signal Error for {instance.transaction_id}: {str(e)}")