import json
from rest_framework import status
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .serializers import CustomUserCreateSerializer
from djoser.views import UserViewSet
from .models import User


class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == "create":
            return CustomUserCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract phone fields explicitly
        phone_number = serializer.validated_data.get("phone_number")
        country_code = serializer.validated_data.get("country_code", "+977")

        # Save user with phone data and is_verified=False
        user = serializer.save(
            is_verified=False,
            phone_number=phone_number,
            country_code=country_code,
        )  # Ensure user is not verified at creation

        # Generate OTP and email verification token
        otp = f"{get_random_string(length=6, allowed_chars='0123456789')}"
        token = get_random_string(64)

        user.otp_code = otp
        user.otp_created_at = timezone.now()
        user.email_verification_token = token
        user.save()

        # # Send OTP email
        # send_mail(
        #     subject="Your OTP Code",
        #     message=f"Your OTP code is: {otp}. It expires in 10 minutes.",
        #     from_email="no-reply@example.com",
        #     recipient_list=[user.email],
        #     fail_silently=False,
        # )

        # Send email verification link
        verification_url = request.build_absolute_uri(
            reverse("verify-email", kwargs={"token": token})
        )
        send_mail(
            subject="Verify your email",
            message=f"Your OTP code is: {otp}. It expires in 10 minutes or Click the link to verify your email: {verification_url}",
            from_email="noreply@example.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


def verify_email(request, token):
    user = get_object_or_404(User, email_verification_token=token)
    user.is_verified = True
    user.email_verification_token = None
    user.otp_code = None
    user.otp_created_at = None
    user.save()
    return HttpResponse("Email verified successfully. You can now log in.")


@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        email = data.get("email")
        otp = data.get("otp")

        if not email or not otp:
            return JsonResponse({"error": "Email and OTP are required"}, status=400)

        user = User.objects.filter(email=email).first()
        if user and user.otp_code == otp and user.otp_is_valid():
            user.is_verified = True
            user.otp_code = None
            user.otp_created_at = None
            user.email_verification_token = None
            user.save()
            return JsonResponse({"message": "OTP verified successfully"}, status=200)
        else:
            return JsonResponse({"error": "Invalid or expired OTP"}, status=400)

    # For any method other than POST, return 405 Method Not Allowed
    return HttpResponseNotAllowed(["POST"])
