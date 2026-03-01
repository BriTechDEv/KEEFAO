from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
    MpesaPaymentView, 
    MpesaCallbackView, 
    StripePaymentView, 
    StripeWebhookView 
)

urlpatterns = [
    path("mpesa/", MpesaPaymentView.as_view(), name="mpesa-initiate"),
    # Externally called endpoints MUST be csrf_exempt
    path("mpesa/callback/", csrf_exempt(MpesaCallbackView.as_view()), name="mpesa-callback"),
    path("stripe/", StripePaymentView.as_view(), name="stripe-initiate"),
    path("stripe/webhook/", csrf_exempt(StripeWebhookView.as_view()), name="stripe-webhook"),
]