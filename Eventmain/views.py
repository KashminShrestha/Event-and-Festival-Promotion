import requests
from django.conf import settings
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Event
from .serializers import EventSerializer
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions


class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        organizer = self.get_object()
        if organizer.status == "approved":
            return Response(
                {"detail": "Organizer already approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        organizer.status = "approved"
        organizer.verified_by = request.user
        organizer.save()
        return Response(
            {"detail": "Organizer approved successfully."}, status=status.HTTP_200_OK
        )


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Event.objects.all()
        if hasattr(user, "organizer_profile"):
            return Event.objects.filter(organizer=user.organizer_profile)
        return Event.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        # Make sure user has an organizer profile
        organizer = getattr(user, "organizer_profile", None)
        if not organizer:
            raise PermissionDenied("You are not registered as an organizer.")

        # Check if the organizer is approved
        if organizer.status.strip().lower() != "approved":
            raise PermissionDenied("Organizer is not approved to create events.")

        # Save with organizer
        serializer.save(organizer=organizer)

    def perform_update(self, serializer):
        event = self.get_object()
        user = self.request.user

        if event.organizer.user != user:
            raise PermissionDenied("You do not own this event.")
        if event.status not in ["draft", "cancelled"]:
            raise PermissionDenied("Event cannot be edited in its current state.")

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user

        if event.organizer.user != user:
            raise PermissionDenied("You do not own this event.")
        if event.status not in ["draft", "cancelled"]:
            raise PermissionDenied("Event cannot be deleted in its current state.")

        return super().destroy(request, *args, **kwargs)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


import io
import qrcode
from django.core.files.base import ContentFile
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="khalti/verify",
        serializer_class=KhaltiPaymentSerializer,
    )
    def khalti_verify(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        amount = serializer.validated_data["amount"]
        booking_id = serializer.validated_data["booking_id"]

        # Use sandbox credentials and endpoint
        khalti_verify_url = getattr(
            settings, "KHALTI_VERIFY_URL", "https://khalti.com/api/v2/payment/verify/"
        )
        khalti_secret_key = getattr(settings, "KHALTI_SECRET_KEY", "test_secret_key")

        payload = {"token": token, "amount": amount}
        headers = {"Authorization": f"Key {khalti_secret_key}"}

        response = requests.post(khalti_verify_url, data=payload, headers=headers)
        if response.status_code == 200 and response.json().get("idx"):
            # Payment successful
            try:
                booking = Booking.objects.get(pk=booking_id)
                booking.status = "paid"
                booking.save()

                # Generate QR code
                qr_data = f"BookingID:{booking.id}"
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                qr_dir = os.path.join(settings.MEDIA_ROOT, "qrcodes")
                os.makedirs(qr_dir, exist_ok=True)
                qr_filename = f"qr_{booking.id}.png"
                qr_path = os.path.join(qr_dir, qr_filename)
                img.save(qr_path)

                # Save QRCode record
                QRCode.objects.create(
                    booking_id=booking,
                    qr_code_path=os.path.join("qrcodes", qr_filename),
                )

                return Response(
                    {
                        "status": "success",
                        "qr_code": settings.MEDIA_URL + "qrcodes/" + qr_filename,
                    }
                )
            except Booking.DoesNotExist:
                return Response(
                    {"status": "failed", "message": "Booking not found."}, status=404
                )
        else:
            return Response(
                {"status": "failed", "message": response.json()}, status=400
            )


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


def khalti_test_view(request):
    return render(request, "khalti_test.html")
