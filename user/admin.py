from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "id",
        "name",
        "is_staff",
        "is_active",
        "is_verified",
        "is_approved",
        "otp_code",
        # "country_code",
        "phone_number",
        # 'email_verification_token',
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_verified",
        "is_active",
        "language",
        "role",
    )
    search_fields = ("email", "name", "phone_number")
    readonly_fields = ("created_at",)
    ordering = ("email",)
    list_per_page = 25
    fieldsets = (
        (
            None,
            {"fields": ("email", "password", "name", "role", "language", "created_at")},
        ),
        ("Phone", {"fields": ("country_code", "phone_number")}),
        (
            "Verification",
            {
                "fields": (
                    "is_verified",
                    "otp_code",
                    "otp_created_at",
                    "email_verification_token",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")},
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        # Only superuser can change is_verified
        ro_fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            ro_fields.append("is_verified")
        return ro_fields

    def save_model(self, request, obj, form, change):
        # Prevent non-superadmins from changing is_verified
        if not request.user.is_superuser and "is_verified" in form.changed_data:
            form.cleaned_data["is_verified"] = obj.is_verified  # revert change
        super().save_model(request, obj, form, change)


admin.site.register(User, CustomUserAdmin)
