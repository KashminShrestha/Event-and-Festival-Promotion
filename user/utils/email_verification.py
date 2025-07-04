from datetime import timedelta
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from firebase.models import User


def send_verification_email(request, user, email_subject="Verify your email"):
    # Generate OTP and token
    otp = f"{get_random_string(length=6, allowed_chars='0123456789')}"
    token = get_random_string(64)

    user.otp_code = otp
    user.otp_created_at = timezone.now()
    user.email_verification_token = token
    user.save()

    # Build verification URL
    verification_url = request.build_absolute_uri(
        reverse("verify-email", kwargs={"token": token})
    )

    # Prepare email content
    context = {
        "otp": otp,
        "verification_url": verification_url,
        "user": user,
    }
    html_message = render_to_string("user/verification_email.html", context)
    plain_message = f"Your OTP code is: {otp}. It expires in 10 minutes. Or click the link to verify your email: {verification_url}"

    email = EmailMultiAlternatives(
        subject=email_subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_message, "text/html")

    try:
        email.send()
        print(f"✅ Verification email sent to {user.email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

    return otp, token, verification_url


def verify_email(request, token):
    try:
        user = User.objects.get(email_verification_token=token)
    except User.DoesNotExist:
        return HttpResponseBadRequest("Invalid verification link.")

    # Check token expiry
    if not user.otp_created_at or timezone.now() - user.otp_created_at > timedelta(
        minutes=10
    ):
        return HttpResponseBadRequest("Token expired.")

    # Mark user as verified and active
    user.is_active = True
    user.is_verified = True  # if you have this field
    user.email_verification_token = None
    user.otp_code = None
    user.otp_created_at = None
    user.save()

    # Optionally redirect to login or success page
    return render(request, "user/verification_success.html")


def resend_verification_email(request, user, cooldown_minutes=5):
    """
    Resend verification email to the user if cooldown period has passed.
    Returns a dict with 'success' status and message or error.
    """
    if user.is_verified:
        return {"success": False, "message": "User is already verified."}

    cooldown_period = timedelta(minutes=cooldown_minutes)
    if user.otp_created_at and timezone.now() - user.otp_created_at < cooldown_period:
        wait_time = cooldown_period - (timezone.now() - user.otp_created_at)
        total_seconds = int(wait_time.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return {
            "success": False,
            "message": f"Please wait {minutes} minutes and {seconds} seconds before resending verification email.",
        }

    # Call existing send_verification_email to generate OTP and send email
    otp, token, verification_url = send_verification_email(request, user)

    return {
        "success": True,
        "message": "Verification email resent successfully.",
        "otp": otp,  # remove in production for security
        "verification_url": verification_url,
    }
