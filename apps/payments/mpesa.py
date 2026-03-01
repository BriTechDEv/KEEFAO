import requests
import base64
import logging
import time
from datetime import datetime, timezone
from django.conf import settings
from django.db import transaction
from .models import Payment

logger = logging.getLogger("mpesa")

class MpesaService:
    _token = None
    _token_expiry = 0

    @staticmethod
    def get_base_url():
        """Returns the appropriate Safaricom URL based on the environment."""
        if getattr(settings, "MPESA_ENVIRONMENT", "sandbox") == "production":
            return "https://api.safaricom.co.ke"
        return "https://sandbox.safaricom.co.ke"

    @staticmethod
    def get_token():
        """Get a cached OAuth token, refresh if expired."""
        if MpesaService._token and time.time() < MpesaService._token_expiry:
            return MpesaService._token

        url = f"{MpesaService.get_base_url()}/oauth/v1/generate?grant_type=client_credentials"
        try:
            # Using a strict timeout for production stability
            response = requests.get(
                url,
                auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET),
                timeout=15 
            )
            response.raise_for_status()
            data = response.json()
            MpesaService._token = data["access_token"]
            # Buffer of 60 seconds to prevent edge-case expiry
            MpesaService._token_expiry = time.time() + int(data.get("expires_in", 3600)) - 60
            logger.info("MPESA: Access token refreshed successfully.")
            return MpesaService._token
        except Exception as e:
            logger.error("MPESA: Failed to fetch access token", exc_info=True)
            raise Exception("Payment gateway authentication failed.")

    @staticmethod
    def stk_push(phone: str, amount: int, contributor_name: str, category="GENERAL", member=None):
        """
        Initiates an STK push and records the 'Pending' transaction in the DB.
        """
        # 1. Standardize phone to 254 format
        phone_digits = "".join(filter(str.isdigit, phone))
        if phone_digits.startswith("0"):
            phone_digits = f"254{phone_digits[1:]}"
        elif len(phone_digits) == 9:
            phone_digits = f"254{phone_digits}"

        if len(phone_digits) != 12:
            raise ValueError(f"Invalid phone number format: {phone}")

        # 2. Generate security credentials
        timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d%H%M%S")
        password_str = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()

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

        # 3. Call Safaricom and Log to DB
        token = MpesaService.get_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.post(
                f"{MpesaService.get_base_url()}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers,
                timeout=25
            )
            response.raise_for_status()
            result = response.json()

            # Ensure the Payment record is created only if Safaricom accepted the request
            if result.get("ResponseCode") == "0":
                with transaction.atomic():
                    Payment.objects.create(
                        user=member,
                        contributor_name=contributor_name,
                        phone=phone_digits,
                        amount=amount,
                        method="mpesa",
                        transaction_id=result.get("CheckoutRequestID"),
                        status="pending",
                        metadata={"category": category}
                    )
            
            return result

        except requests.RequestException as e:
            logger.error(f"MPESA: STK Push request failed for {phone_digits}", exc_info=True)
            raise Exception("We couldn't reach M-Pesa. Please try again in a moment.")