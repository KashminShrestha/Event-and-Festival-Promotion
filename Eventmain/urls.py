from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'organizers', OrganizerViewSet)
router.register(r'events', EventViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'media', MediaViewSet)
router.register(r'auditlogs', AuditLogViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'qrcodes', QRCodeViewSet)
router.register(r'analytics', EventAnalyticsViewSet)
router.register(r'reviews', EventReviewViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
