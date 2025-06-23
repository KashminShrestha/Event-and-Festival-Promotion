import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import action
from djoser.views import TokenCreateView
from user.utils.email_verification import (
    resend_verification_email,
    send_verification_email,
)

from .serializers import (
    AdminUserCreateSerializer,
    CustomUserCreateSerializer,
    PasswordChangeSerializer,
    StaffTokenCreateSerializer,
)
from djoser.views import UserViewSet
from .models import User
from django.contrib.auth import get_user_model


class AdminRegisterAPIView(APIView):
    permission_classes = []  # Adjust permissions as needed

    def post(self, request):
        serializer = AdminUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate OTP and email verification token
        send_verification_email(request, user, email_subject="Verify your admin email")

        return Response(
            {
                "message": "Admin user registered successfully. Verification email sent.",
                "user_id": user.id,
            },
            status=status.HTTP_201_CREATED,
        )


class StaffApprovalViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["post"], url_path="approve")
    def approve(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"error": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id, is_staff=True)
        except User.DoesNotExist:
            return Response(
                {"error": "Staff user not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Check if email is verified before approving
        if not user.is_verified:
            return Response(
                {"error": "User's email is not verified. Approval denied."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_approved = True
        user.save()

        return Response(
            {"message": f"User {user.email} approved successfully."},
            status=status.HTTP_200_OK,
        )


class StaffLoginAPIView(TokenCreateView):
    serializer_class = StaffTokenCreateSerializer


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
        send_verification_email(request, user)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


User = get_user_model()


class VerifyOTPAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response(
                {"error": "Email and OTP are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()
        if user and user.otp_code == otp and user.otp_is_valid():
            user.is_verified = True
            user.otp_code = None
            user.otp_created_at = None
            user.email_verification_token = None
            user.save()
            return Response(
                {"message": "OTP verified successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST
            )


class VerificationResendViewSet(viewsets.ViewSet):
    """
    ViewSet to resend verification emails for both Admin and regular users.
    Use query param `?admin=true` to resend for admin users.
    """

    permission_classes = []  # Adjust as needed

    @action(detail=False, methods=["post"], url_path="resend-verification")
    def resend_verification(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        is_admin = request.query_params.get("admin", "false").lower() == "true"

        try:
            if is_admin:
                # Filter only admin/staff users
                user = User.objects.get(email=email, is_staff=True)
            else:
                # Regular users (non-staff)
                user = User.objects.get(email=email, is_staff=False)
        except User.DoesNotExist:
            return Response(
                {"error": "Admin user not found." if is_admin else "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        result = resend_verification_email(request, user)
        if result["success"]:
            return Response({"message": result["message"]}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": result["message"]}, status=status.HTTP_400_BAD_REQUEST
            )


class PasswordChangeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"message": "Password updated successfully."}, status=status.HTTP_200_OK
        )
