from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Event
from .serializers import EventSerializer
from rest_framework import viewsets
from .models import (
    Organizer, Event, Ticket, Booking, Media, AuditLog,
    Notification, QRCode, EventAnalytics, EventReview
)
from .serializers import (
    OrganizerSerializer, EventSerializer, TicketSerializer, BookingSerializer,
    MediaSerializer, AuditLogSerializer, NotificationSerializer, QRCodeSerializer,
    EventAnalyticsSerializer, EventReviewSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions

class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        organizer = self.get_object()
        if organizer.status == 'approved':
            return Response({'detail': 'Organizer already approved.'}, status=status.HTTP_400_BAD_REQUEST)

        organizer.status = 'approved'
        organizer.verified_by = request.user
        organizer.save()
        return Response({'detail': 'Organizer approved successfully.'}, status=status.HTTP_200_OK)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Event.objects.all()
        if hasattr(user, 'organizer_profile'):
            return Event.objects.filter(organizer=user.organizer_profile)
        return Event.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        # Make sure user has an organizer profile
        organizer = getattr(user, 'organizer_profile', None)
        if not organizer:
            raise PermissionDenied("You are not registered as an organizer.")

        # Check if the organizer is approved
        if organizer.status.strip().lower() != 'approved':
            raise PermissionDenied("Organizer is not approved to create events.")

        # Save with organizer
        serializer.save(organizer=organizer)

    def perform_update(self, serializer):
        event = self.get_object()
        user = self.request.user

        if event.organizer.user != user:
            raise PermissionDenied("You do not own this event.")
        if event.status not in ['draft', 'cancelled']:
            raise PermissionDenied("Event cannot be edited in its current state.")

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user

        if event.organizer.user != user:
            raise PermissionDenied("You do not own this event.")
        if event.status not in ['draft', 'cancelled']:
            raise PermissionDenied("Event cannot be deleted in its current state.")

        return super().destroy(request, *args, **kwargs)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    parser_classes = [MultiPartParser, FormParser]  # Enables file upload
    permission_classes = [IsAuthenticated]

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class QRCodeViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer

class EventAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = EventAnalytics.objects.all()
    serializer_class = EventAnalyticsSerializer

class EventReviewViewSet(viewsets.ModelViewSet):
    queryset = EventReview.objects.all()
    serializer_class = EventReviewSerializer
