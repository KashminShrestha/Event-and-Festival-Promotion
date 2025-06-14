from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from djoser.serializers import UserCreateSerializer
from djoser.serializers import TokenCreateSerializer
from rest_framework.exceptions import ValidationError

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException


# User = get_user_model()


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

        User = get_user_model()
        country_code_input = self.initial_data.get("country_code", None)

        try:
            parsed_number = phonenumbers.parse(value, None)

            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("Invalid phone number.")

            # Extract the country code from the parsed phone number (e.g. 977, 1, etc)
            phone_country_code = f"+{parsed_number.country_code}"

            # Check if input country_code matches the phone number country code
            if country_code_input and country_code_input != phone_country_code:
                raise serializers.ValidationError(
                    f"Country code '{country_code_input}' does not match phone number country code '{phone_country_code}'."
                )

            normalized_number = phonenumbers.format_number(
                parsed_number, phonenumbers.PhoneNumberFormat.E164
            )

            if User.objects.filter(phone_number=normalized_number).exists():
                raise serializers.ValidationError(
                    "This phone number is already registered."
                )

            return normalized_number

        except NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")


class VerifiedUserTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
            raise ValidationError("Your email is not verified. Please verify to login.")
        return data
