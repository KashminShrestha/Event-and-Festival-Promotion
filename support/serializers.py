from rest_framework import serializers
from .models import FAQ, SupportRequest, ContactInfo


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"

    def validate_question(self, value):
        if not value.strip():
            raise serializers.ValidationError("Question field cannot be empty.")
        return value


class SupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = "__all__"

    def validate(self, attrs):
        if not attrs.get("status") or not attrs["status"].strip():
            raise serializers.ValidationError(
                {"status": "status cannot be empty."}
            )
        return attrs


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = "__all__"
