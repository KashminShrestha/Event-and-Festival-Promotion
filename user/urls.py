from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminRegisterAPIView,
    CustomUserViewSet,
    PasswordChangeAPIView,
    StaffLoginAPIView,
    VerificationResendViewSet,
    VerifyOTPAPIView,
    StaffApprovalViewSet,
)
from .utils.email_verification import verify_email

router = DefaultRouter()
router.register(r"staff-approval", StaffApprovalViewSet, basename="staff-approval")
router.register(r"resend-otp", VerificationResendViewSet, basename="resend-otp")

urlpatterns = [
    path("auth/users/", CustomUserViewSet.as_view({"post": "create"}), name="register"),
    path("verify-email/<str:token>/", verify_email, name="verify-email"),
    path("verify-otp/", VerifyOTPAPIView.as_view(), name="verify-otp"),
    path(
        "auth/change-password/", PasswordChangeAPIView.as_view(), name="change-password"
    ),
    path("admin/register/", AdminRegisterAPIView.as_view(), name="admin-register"),
    path("admin/login/", StaffLoginAPIView.as_view(), name="admin-login"),
    path("", include(router.urls)),  # Include the router-generated URLs
]
