import stripe
import base64
import requests
import logging
import time
import uuid
from datetime import datetime, timezone
from django.conf import settings
from django.db import transaction
from .models import Payment
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

mpesa_logger = logging.getLogger("mpesa")
stripe_logger = logging.getLogger("stripe")

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentService:
    """Unified payment service for Mpesa and Stripe."""

    _mpesa_token = None
    _mpesa_token_expiry = 0

    @staticmethod
    def _get_mpesa_base_url():
        """Switch between Sandbox and Production URLs based on settings."""
        if getattr(settings, "MPESA_ENVIRONMENT", "sandbox") == "production":
            return "https://api.safaricom.co.ke"
        return "https://sandbox.safaricom.co.ke"

    @staticmethod
    def _get_mpesa_token():
        if PaymentService._mpesa_token and time.time() < PaymentService._mpesa_token_expiry:
            return PaymentService._mpesa_token

        url = f"{PaymentService._get_mpesa_base_url()}/oauth/v1/generate?grant_type=client_credentials"
        try:
            response = requests.get(
                url,
                auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET),
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            PaymentService._mpesa_token = data["access_token"]
            PaymentService._mpesa_token_expiry = time.time() + int(data.get("expires_in", 3600)) - 60
            return PaymentService._mpesa_token
        except Exception as e:
            mpesa_logger.error("MPESA: Failed to fetch token", exc_info=True)
            raise Exception("Payment gateway authentication failed.")

    @staticmethod
    def mpesa_push(phone: str, amount: int, contributor_name: str, category="MONTHLY", member=None):
        """Triggers M-Pesa STK Push and logs the transaction."""
        # 1. Standardize Phone Number
        phone_digits = "".join(filter(str.isdigit, phone))
        if phone_digits.startswith("0"):
            phone_digits = f"254{phone_digits[1:]}"
        elif len(phone_digits) == 9:
            phone_digits = f"254{phone_digits}"

        if len(phone_digits) != 12:
            raise ValueError("Invalid phone format. Use 254XXXXXXXXX")

        # 2. Setup Credentials
        token = PaymentService._get_mpesa_token()
        timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d%H%M%S")
        password_str = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()

        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_digits,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone_digits,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": f"KEEFAO-{category[:5]}",
            "TransactionDesc": f"{category} Contribution",
        }

        # 3. Request Push and Log to DB
        try:
            response = requests.post(
                f"{PaymentService._get_mpesa_base_url()}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers,
                timeout=20
            )
            response.raise_for_status()
            result = response.json()
            
            checkout_id = result.get("CheckoutRequestID", str(uuid.uuid4()))

            # Use an atomic transaction to ensure DB consistency
            with transaction.atomic():
                Payment.objects.create(
                    transaction_id=checkout_id,
                    contributor_name=contributor_name,
                    phone=phone_digits,
                    amount=amount,
                    method="mpesa",
                    status="pending",
                    user=member, 
                    metadata={
                        "category": category,
                        "member_id": member.id if member else None,
                    }
                )
            return result

        except Exception as e:
            mpesa_logger.error(f"MPESA: STK Push failed for {phone_digits}", exc_info=True)
            raise Exception("M-Pesa service is currently unavailable. Please try again.")

    @staticmethod
    def stripe_checkout(amount: int, email: str, contributor_name: str, category="MONTHLY", member=None):
        """Creates a Stripe Checkout Session."""
        try:
            with transaction.atomic():
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[{
                        "price_data": {
                            "currency": "kes",
                            "product_data": {
                                "name": f"KEEFAO {category.title()} Contribution",
                                "description": f"Contribution by {contributor_name}"
                            },
                            "unit_amount": int(amount * 100),
                        },
                        "quantity": 1,
                    }],
                    mode="payment",
                    success_url=f"{settings.DOMAIN}/payment-success?session_id={{CHECKOUT_SESSION_ID}}",
                    cancel_url=f"{settings.DOMAIN}/payment-failed",
                    customer_email=email,
                    metadata={
                        "category": category,
                        "member_id": member.id if member else None,
                        "contributor_name": contributor_name
                    }
                )
                
                # Log the Stripe payment attempt
                Payment.objects.create(
                    transaction_id=session.id,
                    contributor_name=contributor_name,
                    email=email,
                    amount=amount,
                    method="stripe",
                    status="pending",
                    user=member,
                    metadata={
                        "category": category,
                        "member_id": member.id if member else None
                    }
                )
            return session
        except Exception as e:
            stripe_logger.error(f"STRIPE: Session creation failed for {email}", exc_info=True)
            raise Exception("Secure card payment setup failed.")