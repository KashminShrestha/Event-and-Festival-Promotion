from rest_framework import serializers
from django.contrib.auth import get_user_model

from user.utils.phonenumber_validation import validate_phone_number
from .models import *
from djoser.serializers import UserCreateSerializer
from djoser.serializers import TokenCreateSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

# User = get_user_model()


class AdminUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "password",
            "re_password",
            "phone_number",
            "country_code",
        )

    def validate(self, attrs):
        password = attrs.get("password")
        re_password = attrs.get("re_password")

        if password != re_password:
            raise serializers.ValidationError(
                {"re_password": "Password fields didn't match."}
            )
        validate_password(password)

        return attrs

    def validate_phone_number(self, value):
        country_code_input = self.initial_data.get("country_code", None)
        return validate_phone_number(value, country_code_input)

    def create(self, validated_data):
        validated_data = validated_data.copy()
        validated_data.pop("email", None)
        validated_data.pop("password", None)
        validated_data.pop("re_password", None)
        validated_data.pop("phone_number", None)
        validated_data.pop("country_code", None)

        user = User.objects.create_user(
            email=self.validated_data["email"],
            password=self.validated_data["password"],
            phone_number=self.validated_data.get("phone_number"),
            country_code=self.validated_data.get("country_code", "+977"),
            is_staff=True,
            is_approved=False,
            **validated_data,
        )
        return user


class StaffTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_staff:
            raise ValidationError("User does not have staff privileges.")

        if not user.is_verified:
            raise ValidationError("User email is not verified.")

        if not user.is_approved:
            raise ValidationError("Staff user is not approved yet.")

        return data


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = (
            "id",
            "name",
            "email",
            "password",
            "phone_number",
            "country_code",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_phone_number(self, value):
        country_code_input = self.initial_data.get("country_code", None)
        return validate_phone_number(value, country_code_input)


class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_verified:
            raise serializers.ValidationError("User email is not verified.")

        if user.is_staff and not user.is_approved:
            raise serializers.ValidationError(
                "Staff user is not approved by superadmin yet."
            )
        return data


class VerifiedUserTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
            raise ValidationError("Your email is not verified. Please verify to login.")
        return data
