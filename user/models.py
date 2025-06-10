from django.db import models
from django.contrib.auth.models import Group, AbstractUser, BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be entered in the format: '+999'. Up to 15 digits allowed.",
)


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        password=None,
        phone_number=None,
        country_code="+977",
        **extra_fields,
    ):
        if not email:
            raise ValueError("The Email field must be set")
        # Require phone number only if not superuser
        if not phone_number and not extra_fields.get("is_superuser", False):
            raise ValueError("The Phone number must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone_number=phone_number,
            country_code=country_code,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Pass phone_number=None explicitly to bypass requirement in create_user
        return self.create_user(email, password, phone_number=None, **extra_fields)


class User(AbstractUser):
    LANGUAGE_CHOICES = (
        ("en", "English"),
        ("np", "Nepali"),
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        Group,
        related_name="user_role",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="en")
    created_at = models.DateTimeField(auto_now_add=True)

    # Phone-related fields
    country_code = models.CharField(max_length=5, default="+977")  # Default Nepal
    phone_number = models.CharField(
        validators=[phone_regex], max_length=15, blank=True, null=True
    )

    # New fields for verification
    is_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    email_verification_token = models.CharField(max_length=64, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def otp_is_valid(self, expiry_minutes=10):
        """Check if the OTP is still valid."""
        if self.otp_created_at:
            return timezone.now() <= self.otp_created_at + timezone.timedelta(
                minutes=expiry_minutes
            )
        return False

    @property
    def full_phone_number(self):
        """Returns E.164 formatted phone number (e.g., '+9779812345678')"""
        return f"{self.country_code}{self.phone_number}" if self.phone_number else None
