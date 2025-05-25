import requests
import io
import qrcode
from django.core.files.base import ContentFile
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Event
from .serializers import EventSerializer
from rest_framework import viewsets
from .models import *
from .serializers import *
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions



class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        organizer = self.get_object()
        if organizer.status == "approved":
            return Response(
                {"detail": "Organizer already approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if organizer.status == "approved":
            return Response(
                {"detail": "Organizer already approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        organizer.status = "approved"
        organizer.status = "approved"
        organizer.verified_by = request.user
        organizer.save()
        return Response(
            {"detail": "Organizer approved successfully."}, status=status.HTTP_200_OK
        )

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


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def verify_payment(self, request, pk=None):
        booking = self.get_object()
        token = request.data.get("token")
        amount = request.data.get("amount")

        print(f"Received token: {token}, amount: {amount}")  # Debug print

        if not token or not amount:
            return Response(
                {"detail": "Token and amount required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        verify_url = getattr(settings, "KHALTI_VERIFY_URL", None)
        if not verify_url:
            return Response(
                {"detail": "Khalti verify URL not configured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        headers = {"Authorization": f"Key {settings.KHALTI_SECRET_KEY}"}
        payload = {"token": token, "amount": int(amount)}

        resp = requests.post(verify_url, headers=headers, json=payload)
        data = resp.json()

        print("Khalti response:", data)  # Debug print

        # Khalti returns status "OK" on success in 'status' field
        if resp.status_code == 200 and data.get("status") == "OK":
            booking.status = "paid"
            # Prefer 'idx' from root or inside 'details'
            booking.transaction_id = data.get("idx") or data.get("details", {}).get(
                "idx"
            )
            booking.save()

            # Generate QR code
            qr = qrcode.make(
                f"BookingID:{booking.id};TransactionID:{booking.transaction_id}"
            )

            # Save QR code image to QRCode model
            buffer = io.BytesIO()
            qr.save(buffer)
            buffer.seek(0)
            filename = f"booking_{booking.id}_qr.png"
            qr_image_file = ContentFile(buffer.read(), filename)

            qr_code_obj = QRCode.objects.create(
                booking=booking,
                qr_image=qr_image_file,
            )

            # TODO: Send notification/email if needed

            return Response({"detail": "Payment verified and booking confirmed."})

        else:
            return Response(
                {"detail": "Payment verification failed.", "error": data},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @staticmethod
    def refund_booking(booking, amount=None, mobile=None):
        refund_url = f"https://khalti.com/api/merchant-transaction/{booking.transaction_id}/refund/"
        headers = {"Authorization": f"Key {settings.KHALTI_SECRET_KEY}"}
        payload = {}

        if mobile:
            payload["mobile"] = mobile
        if amount:
            payload["amount"] = int(amount)  # amount in paisa

        response = requests.post(refund_url, headers=headers, json=payload)
        if response.status_code == 200:
            booking.status = "refunded"
            booking.save()
            return True
        return False

    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def verify_payment(self, request, pk=None):
        booking = self.get_object()
        token = request.data.get("token")
        amount = request.data.get("amount")

        print(f"Received token: {token}, amount: {amount}")  # Debug print

        if not token or not amount:
            return Response(
                {"detail": "Token and amount required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        verify_url = getattr(settings, "KHALTI_VERIFY_URL", None)
        if not verify_url:
            return Response(
                {"detail": "Khalti verify URL not configured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        headers = {"Authorization": f"Key {settings.KHALTI_SECRET_KEY}"}
        payload = {"token": token, "amount": int(amount)}

        resp = requests.post(verify_url, headers=headers, json=payload)
        data = resp.json()

        print("Khalti response:", data)  # Debug print

        # Khalti returns status "OK" on success in 'status' field
        if resp.status_code == 200 and data.get("status") == "OK":
            booking.status = "paid"
            # Prefer 'idx' from root or inside 'details'
            booking.transaction_id = data.get("idx") or data.get("details", {}).get(
                "idx"
            )
            booking.save()

            # Generate QR code
            qr = qrcode.make(
                f"BookingID:{booking.id};TransactionID:{booking.transaction_id}"
            )

            # Save QR code image to QRCode model
            buffer = io.BytesIO()
            qr.save(buffer)
            buffer.seek(0)
            filename = f"booking_{booking.id}_qr.png"
            qr_image_file = ContentFile(buffer.read(), filename)

            qr_code_obj = QRCode.objects.create(
                booking=booking,
                qr_image=qr_image_file,
            )

            # TODO: Send notification/email if needed

            return Response({"detail": "Payment verified and booking confirmed."})

        else:
            return Response(
                {"detail": "Payment verification failed.", "error": data},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @staticmethod
    def refund_booking(booking, amount=None, mobile=None):
        refund_url = f"https://khalti.com/api/merchant-transaction/{booking.transaction_id}/refund/"
        headers = {"Authorization": f"Key {settings.KHALTI_SECRET_KEY}"}
        payload = {}

        if mobile:
            payload["mobile"] = mobile
        if amount:
            payload["amount"] = int(amount)  # amount in paisa

        response = requests.post(refund_url, headers=headers, json=payload)
        if response.status_code == 200:
            booking.status = "refunded"
            booking.save()
            return True
        return False


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


def khalti_test_view(request):
    return render(request, "khalti_test.html")

def khalti_test_view(request):
    return render(request, 'khalti_test.html')