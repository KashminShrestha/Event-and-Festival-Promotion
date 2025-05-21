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

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("end_time must be after start_time.")
        return data    

# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = '__all__'
# 
    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("end_time must be after start_time.")
        return data    

# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = '__all__'
#     read_only_fields = ['organizer'] 

from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'event', 'name', 'price', 'quantity', 'ticket_type', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        # For PATCH: Use existing instance values if not provided in data
        instance = getattr(self, 'instance', None)
        ticket_type = data.get('ticket_type', getattr(instance, 'ticket_type', None))
        if ticket_type not in dict(Ticket.TICKET_TYPE_CHOICES):
            raise serializers.ValidationError("Invalid ticket type.")

        quantity = data.get('quantity', getattr(instance, 'quantity', None))
        if quantity is None or quantity <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")

        event = data.get('event', getattr(instance, 'event', None))
        if not event:
            raise serializers.ValidationError("Event must be specified.")

        # Calculate total quantity of existing tickets for this event excluding the current instance if updating
        existing_tickets = Ticket.objects.filter(event=event)
        if instance:
            existing_tickets = existing_tickets.exclude(pk=instance.pk)

        total_quantity = sum(ticket.quantity for ticket in existing_tickets) + quantity

        if total_quantity > event.capacity:
            raise serializers.ValidationError(
                f"Total ticket quantity ({total_quantity}) exceeds event capacity ({event.capacity})."
            )

        return data


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
