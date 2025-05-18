from rest_framework import serializers
from .models import *

# serializers.py
class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'

    def validate(self, data):
        # You can optionally add checks here
        return data

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
    read_only_fields = ['organizer'] 

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'


class EventAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAnalytics
        fields = '__all__'


class EventReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventReview
        fields = '__all__'
