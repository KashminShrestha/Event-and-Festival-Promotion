from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .views import verify_email, verify_otp
from user.views import CustomUserViewSet


urlpatterns = [
    path("auth/users/", CustomUserViewSet.as_view({"post": "create"}), name="register"),
    path("verify-email/<str:token>/", verify_email, name="verify-email"),
    path("verify-otp/", verify_otp, name="verify-otp"),
]
