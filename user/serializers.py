from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from djoser.serializers import UserCreateSerializer
from djoser.serializers import TokenCreateSerializer
from rest_framework.exceptions import ValidationError

# User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ("id", "name", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}


class VerifiedUserTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
            raise ValidationError("Your email is not verified. Please verify to login.")
        return data
