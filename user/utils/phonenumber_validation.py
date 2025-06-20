import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


def validate_phone_number(value, country_code_input=None):
    try:
        parsed_number = phonenumbers.parse(value, None)

        if not phonenumbers.is_valid_number(parsed_number):
            raise serializers.ValidationError("Invalid phone number.")

        phone_country_code = f"+{parsed_number.country_code}"

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
