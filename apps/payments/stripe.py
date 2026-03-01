import stripe
from django.conf import settings
from django.db import transaction
from .models import Payment
import logging

logger = logging.getLogger("stripe")

# Use the secret key from settings
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    @staticmethod
    def create_checkout_session(amount: int, email: str, contributor_name: str, category="MONTHLY", member=None):
        """
        Creates a Stripe Checkout Session and logs a pending Payment record.
        """
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        try:
            # 1. Define the Session
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "kes",
                        "product_data": {
                            "name": f"KEEFAO {category.title()} Contribution",
                            "description": f"Contribution by {contributor_name}",
                        },
                        "unit_amount": int(amount * 100), # Stripe expects cents/cents-equivalent
                    },
                    "quantity": 1,
                }],
                mode="payment",
                # These URLs should be defined in your settings.py
                success_url=f"{settings.DOMAIN}/payment-success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.DOMAIN}/payment-failed",
                customer_email=email,
                # Metadata is key: This is sent back in the webhook to update the DB
                metadata={
                    "category": category,
                    "member_id": member.id if member else None,
                    "contributor_name": contributor_name
                }
            )

            # 2. Log the transaction to our database before redirecting the user
            with transaction.atomic():
                Payment.objects.create(
                    user=member,
                    contributor_name=contributor_name,
                    email=email,
                    amount=amount,
                    method="stripe",
                    transaction_id=session.id, # We track by Stripe Session ID
                    status="pending",
                    metadata={
                        "category": category,
                        "member_id": member.id if member else None
                    }
                )

            logger.info(f"Stripe: Session created for {email} - {amount} KES")
            return session

        except stripe.error.StripeError as e:
            logger.error(f"Stripe API Error: {str(e)}", exc_info=True)
            raise Exception("Secure card payment is currently unavailable.")
        except Exception as e:
            logger.error(f"Stripe Service Error: {str(e)}", exc_info=True)
            raise Exception("An internal error occurred while processing your payment.")