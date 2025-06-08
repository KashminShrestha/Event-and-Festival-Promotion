from datetime import timezone
import requests
import base64
import io
import qrcode
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files.storage import default_storage
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.conf import settings
from django.shortcuts import redirect, render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Event, Booking, QRCode
from .serializers import EventSerializer, BookingSerializer
from .models import *
from .serializers import *
from .models import *
from .serializers import *
from rest_framework import status, permissions
from .models import AuditLog
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage



class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
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
        # Audit log
        AuditLog.objects.create(
            admin=request.user,
            action="Approved organizer",
            target_type="Organizer",
            target_id=organizer.id,
        )
        return Response(
            {"detail": "Organizer approved successfully."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        organizer = self.get_object()
        if organizer.status == "rejected":
            return Response(
                {"detail": "Organizer already rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        organizer.status = "rejected"
        organizer.verified_by = request.user
        organizer.save()
        # Audit log
        AuditLog.objects.create(
            admin=request.user,
            action="Rejected organizer",
            target_type="Organizer",
            target_id=organizer.id,
        )
        return Response({"detail": "Organizer rejected."}, status=status.HTTP_200_OK)


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

    # Multilingual handling methods
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = self._apply_language(serializer.data, request)
        return Response(data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = [self._apply_language(item, request) for item in serializer.data]
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = [self._apply_language(item, request) for item in serializer.data]
        return Response(data)

    def _apply_language(self, data, request):
        """Helper method to handle language switching"""
        lang = request.headers.get("Accept-Language", "en").lower()
        if lang == "ne":
            # Preserve original values while overriding display fields
            data["name_display"] = data.get("name_nep") or data["name"]
            data["description_display"] = (
                data.get("description_nep") or data["description"]
            )
        else:
            data["name_display"] = data["name"]
            data["description_display"] = data["description"]
        return data

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        event = self.get_object()
        if event.status == "published":
            return Response(
                {"detail": "Event already published."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        event.status = "published"
        event.save()
        AuditLog.objects.create(
            admin=request.user,
            action="Approved event",
            target_type="Event",
            target_id=event.id,
        )
        return Response(
            {"detail": "Event approved and published."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        event = self.get_object()
        if event.status == "cancelled":
            return Response(
                {"detail": "Event already cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        event.status = "cancelled"
        event.save()
        AuditLog.objects.create(
            admin=request.user,
            action="Rejected event",
            target_type="Event",
            target_id=event.id,
        )
        return Response(
            {"detail": "Event rejected and cancelled."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def change_status(self, request, pk=None):
        event = self.get_object()
        new_status = request.data.get("status")
        valid_statuses = ["draft", "published", "cancelled"]
        if new_status not in valid_statuses:
            return Response(
                {"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST
            )
        old_status = event.status
        event.status = new_status
        event.save()
        AuditLog.objects.create(
            admin=request.user,
            action=f"Changed event status from {old_status} to {new_status}",
            target_type="Event",
            target_id=event.id,
        )
        return Response(
            {"detail": f"Event status changed to {new_status}."},
            status=status.HTTP_200_OK,
        )


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def create_with_payment(self, request):
        """
        Create booking and initiate Khalti E-Payment.
        This replaces the widget-based approach.
        """
        try:
            # Extract booking data
            print("Khalti Secret Key:", settings.KHALTI_SECRET_KEY)
            ticket_id = request.data.get("ticket_id")
            quantity = request.data.get("quantity")

            if not ticket_id or not quantity:
                return Response(
                    {"error": "ticket_id and quantity are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get ticket and calculate total
            from .models import Ticket

            ticket = Ticket.objects.get(id=ticket_id)
            total_amount = ticket.price * quantity

            # Count how many tickets are already booked (only for 'paid' bookings)
            booked_quantity = (
                Booking.objects.filter(ticket=ticket, status="paid").aggregate(
                    total=models.Sum("quantity")
                )["total"]
                or 0
            )

            remaining_quantity = ticket.quantity - booked_quantity

            # Ensure requested quantity does not exceed remaining
            if quantity > remaining_quantity:
                return Response(
                    {"error": f"Only {remaining_quantity} tickets available."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create booking (status = pending until payment)
            booking = Booking.objects.create(
                user=request.user,
                ticket=ticket,
                quantity=quantity,
                total_amount=total_amount,
                status="pending",  # Will change to 'paid' after callback
                payment_method="khalti",
            )

            # Prepare Khalti E-Payment payload
            payload = {
                "return_url": f"{settings.BASE_URL}/api/bookings/khalti_callback/",
                "website_url": settings.BASE_URL,
                "amount": int(total_amount * 100),  # Convert Rs to paisa
                "purchase_order_id": str(booking.id),
                "purchase_order_name": f"Ticket for {ticket.event.name}",
                "customer_info": {
                    "name": request.user.get_full_name() or request.user.username,
                    "email": request.user.email,
                },
                "amount_breakdown": [
                    {
                        "label": f"{ticket.name} x {quantity}",
                        "amount": int(total_amount * 100),
                    }
                ],
                "product_details": [
                    {
                        "identity": str(ticket.id),
                        "name": ticket.name,
                        "total_price": int(total_amount * 100),
                        "quantity": quantity,
                        "unit_price": int(ticket.price * 100),
                    }
                ],
            }

            headers = {
                "Authorization": f"key {settings.KHALTI_SECRET_KEY}",
                "Content-Type": "application/json",
            }

            # Initiate payment with Khalti
            response = requests.post(
                "https://a.khalti.com/api/v2/epayment/initiate/",
                headers=headers,
                json=payload,
            )

            if response.status_code == 200:
                data = response.json()
                payment_url = data.get("payment_url")

                if payment_url:
                    return Response(
                        {
                            "booking_id": booking.id,
                            "payment_url": payment_url,
                            "message": "Booking created. Please complete payment.",
                        }
                    )
                else:
                    booking.delete()  # Clean up on failure
                    return Response(
                        {"error": "Payment URL not received from Khalti"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                booking.delete()  # Clean up on failure
                return Response(
                    {"error": "Failed to initiate payment", "details": response.text},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["get"])
    def khalti_callback(self, request):
        """
        Handle Khalti's payment callback after user completes payment.
        This replaces manual token verification.
        """
        print("Khalti Callback Received")  # debugging
        # Extract callback parameters
        booking_id = request.GET.get("purchase_order_id")
        payment_status = request.GET.get("status")
        pidx = request.GET.get("pidx")
        amount = request.GET.get("amount")
        tidx = request.GET.get("tidx")

        print(
            f"Khalti Callback: booking_id={booking_id}, status={payment_status}, pidx={pidx}"
        )

        # Validate callback parameters
        if not booking_id or payment_status != "Completed" or not pidx:
            return Response(
                {"error": "Invalid callback parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Verify payment with Khalti
            verification_response = requests.post(
                "https://dev.khalti.com/api/v2/epayment/lookup/",
                json={"pidx": pidx},
                headers={
                    "Authorization": f"key {settings.KHALTI_SECRET_KEY}",
                    "Content-Type": "application/json",
                },
            )

            if verification_response.status_code == 200:
                verification_data = verification_response.json()

                # Check if payment is actually not completed
                if verification_data.get("status") != "Completed":
                    return Response(
                        {"error": "Payment verification failed"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Update booking status
                booking = Booking.objects.get(id=booking_id)
                booking.status = "paid"
                booking.transaction_id = pidx  # Store pidx as transaction_id
                booking.save()

                # Generate QR Code
                # qr_data = f"BookingID:{booking.id};TransactionID:{booking.transaction_id};TIDX:{tidx}"
                # qr = qrcode.make(qr_data)
                qr_data = f"BookingID:{booking.id};TransactionID:{booking.transaction_id};TIDX:{tidx}"
                qr = qrcode.make(qr_data)

                buffer = io.BytesIO()
                qr.save(buffer)
                buffer.seek(0)

                # Encode image to base64
                # qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                # qr_data_uri = f"data:image/png;base64,{qr_base64}"
                # Save only the QR data (not image) 
                QRCode.objects.create(booking=booking, qr_code=qr_data)

                # Save base64 QR code to DB
                # QRCode.objects.create(booking=booking, qr_code=qr_data_uri)

                print(f"✅ Booking {booking.id} payment confirmed and QR saved.")

                # QR code already in buffer
                qr_image_data = buffer.getvalue()

                # Email content
                subject = f"Your Booking Confirmation - {booking.ticket.event.name}"
                to_email = booking.user.email

                # Render optional HTML template
                html_message = render_to_string(
                    "emails/booking_confirmation.html",
                    {
                        "user": booking.user,
                        "booking": booking,
                        "ticket": booking.ticket,
                        "quantity": booking.quantity,
                        "total_amount": booking.total_amount,
                        "qr_image": "qr_data_uri", 
                    },
                )

                # Create email with HTML content
                # email = EmailMessage(
                #     subject,
                #     html_message,
                #     settings.DEFAULT_FROM_EMAIL,
                #     [to_email],
                # )
                email = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, [to_email])
                email.content_subtype = "html"

                # Attach QR code image
                # email.attach("booking_qr.png", qr_image_data, "image/png")
                # email.attach("booking_qr.png", qr_image_data, "image/png")
                
                email.attach_alternative(html_message, "text/html")

                # Embed image using MIMEImage
                qr_image = MIMEImage(qr_image_data)
                qr_image.add_header("Content-ID", "<qr_code_cid>")
                email.attach(qr_image)
                # email.send()

                # Send email
                try:
                    email.send()
                    print(f"✅ Email with QR code sent to {to_email}")
                except Exception as e:
                    print(f"❌ Failed to send email: {e}")

                # Redirect to success page
                frontend_url = getattr(
                    settings, "FRONTEND_URL", "http://localhost:3000"
                )
                return redirect(
                    f"{frontend_url}/booking-success?booking_id={booking.id}"
                )

            else:
                return Response(
                    {
                        "error": "Payment verification failed",
                        "details": verification_response.text,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=["post"])
    def refund_booking(self, request, pk=None):
        """
        Refund a booking (keep your existing logic but update for E-Payment)
        """
        booking = self.get_object()

        if booking.status != "paid":
            return Response(
                {"error": "Only paid bookings can be refunded"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # For E-Payment, use the refund endpoint (if available)
            # Note: You may need to check Khalti's E-Payment refund documentation
            refund_url = "https://test-pay.khalti.com/api/v2/epayment/refund/"
            headers = {"Authorization": f"key {settings.KHALTI_SECRET_KEY}"}
            payload = {
                "pidx": booking.transaction_id,  # Use pidx for E-Payment refunds
                "amount": int(booking.total_amount * 100),  # Amount in paisa
            }

            response = requests.post(refund_url, headers=headers, json=payload)

            if response.status_code == 200:
                booking.status = "refunded"
                booking.save()  # This will trigger refund notification signals

                return Response({"message": "Booking refunded successfully"})
            else:
                return Response(
                    {"error": "Refund failed", "details": response.text},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    parser_classes = [MultiPartParser, FormParser]  # Enables file upload
    permission_classes = [IsAuthenticated]

    # Multilingual handling methods
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = self._apply_language(serializer.data, request)
        return Response(data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = [self._apply_language(item, request) for item in serializer.data]
            return self.get_paginated_response(data)
        serializer = self.get_serializer(queryset, many=True)
        data = [self._apply_language(item, request) for item in serializer.data]
        return Response(data)

    def _apply_language(self, data, request):
        lang = request.headers.get("Accept-Language", "en").lower()
        if lang == "ne":
            data["caption_display"] = data.get("caption_nep") or data.get("caption_eng")
        else:
            data["caption_display"] = data.get("caption_eng") or data.get("caption_nep")
        return data


class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class QRCodeViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer


class EventReviewViewSet(viewsets.ModelViewSet):
    queryset = EventReview.objects.all()
    serializer_class = EventReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = EventAnalytics.objects.all()
    serializer_class = EventAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="increment-view")
    def increment_view(self, request):
        event_id = request.data.get("event")
        user = request.user
        try:
            analytics, created = EventAnalytics.objects.get_or_create(
                event_id=event_id, user=user
            )
            analytics.views += 1
            analytics.last_viewed_at = timezone.now()
            analytics.save()
            return Response({"detail": "View incremented."}, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response(
                {"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=["post"], url_path="increment-click")
    def increment_click(self, request):
        event_id = request.data.get("event")
        user = request.user
        try:
            analytics, created = EventAnalytics.objects.get_or_create(
                event_id=event_id, user=user
            )
            analytics.clicks += 1
            analytics.save()
            return Response({"detail": "Click incremented."}, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response(
                {"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND
            )


def khalti_test_view(request):
    return render(request, "khalti_test.html")
