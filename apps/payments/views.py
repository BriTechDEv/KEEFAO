from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .services import PaymentService
from .models import Payment
import logging
import stripe

mpesa_logger = logging.getLogger("mpesa")
stripe_logger = logging.getLogger("stripe")

# -----------------------------
# M-Pesa Payment Initiation
# -----------------------------
class MpesaPaymentView(APIView):
    def post(self, request):
        data = request.data
        try:
            # We pass the authenticated user and category if available
            result = PaymentService.mpesa_push(
                phone=data.get("phone"),
                amount=int(data.get("amount")),
                contributor_name=data.get("name"),
                category=data.get("category", "MONTHLY"),
                member=request.user if request.user.is_authenticated else None
            )
            return Response(result)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StripePaymentView(APIView):
    def post(self, request):
        data = request.data
        try:
            # expect email for stripe
            result = PaymentService.stripe_checkout(
                amount=int(data.get("amount")),
                email=data.get("email"),
                contributor_name=data.get("name"),
                category=data.get("category", "MONTHLY"),
                member=request.user if request.user.is_authenticated else None,
            )
            return Response({"session": result})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------
# M-Pesa Callback
# -----------------------------
class MpesaCallbackView(APIView):
    def post(self, request):
        data = request.data
        try:
            stk_callback = data.get("Body", {}).get("stkCallback", {})
            checkout_request_id = stk_callback.get("CheckoutRequestID")
            result_code = stk_callback.get("ResultCode")

            # Find the pending payment
            payment = Payment.objects.filter(transaction_id=checkout_request_id).first()
            
            if payment:
                if result_code == 0:
                    payment.status = "completed"
                    payment.save()
                    # TODO: Trigger Contribution update logic here
                    mpesa_logger.info(f"Payment {checkout_request_id} successful.")
                else:
                    payment.status = "failed"
                    payment.save()
                    mpesa_logger.warning(f"Payment {checkout_request_id} failed: {stk_callback.get('ResultDesc')}")
            
        except Exception as e:
            mpesa_logger.error("Error processing Mpesa callback", exc_info=True)

        return Response({"ResultCode": 0, "ResultDesc": "Accepted"})

# -----------------------------
# Stripe Webhook (New & Required)
# -----------------------------
class StripeWebhookView(APIView):
    """
    Stripe sends a POST request here when a payment is successful.
    """
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            transaction_id = session.get("id")
            
            payment = Payment.objects.filter(transaction_id=transaction_id).first()
            if payment:
                payment.status = "completed"
                payment.save()
                # TODO: Trigger Contribution update logic here
                stripe_logger.info(f"Stripe Payment {transaction_id} completed.")

        return Response({"status": "success"})