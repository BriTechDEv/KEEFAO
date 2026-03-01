from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings
from .models import Member

@receiver(post_save, sender=Member)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        subject = "Welcome to KEEFAO Alumni!"
        message = f"Hi {instance.first_name},\n\nWelcome to the KEEFAO Alumni platform! We're glad to have you. Log in to your profile to see your contribution history."
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=True, # Prevents signup crash if email fails
        )


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # The 'token' is what the user needs to provide to the 'confirm' endpoint
    email_plaintext_message = f"Your password reset token is: {reset_password_token.key}"

    send_mail(
        "Password Reset for KEEFAO",
        email_plaintext_message,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email]
    )