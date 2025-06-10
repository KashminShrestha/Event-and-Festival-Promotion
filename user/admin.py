from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "name",
        "is_staff",
        "is_active",
        "language",
        "is_verified",
        'otp_code',
        'country_code',
        'phone_number',
        'email_verification_token',
    )
    list_filter = ("is_staff", "is_active", "language")
    search_fields = ("email", "name")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
