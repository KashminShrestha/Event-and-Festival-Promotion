from django.urls import path
from .views import CustomUserViewSet, verify_email, VerifyOTPAPIView

urlpatterns = [
    path("auth/users/", CustomUserViewSet.as_view({"post": "create"}), name="register"),
    path("verify-email/<str:token>/", verify_email, name="verify-email"),
    path("verify-otp/", VerifyOTPAPIView.as_view(), name="verify-otp"),
]
