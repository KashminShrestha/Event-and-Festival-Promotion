from django.contrib import admin
from .models import *

# Organizer Admin


class CommonAdmin(admin.ModelAdmin):
    list_per_page = 25


class OrganizerAdmin(CommonAdmin):
    list_display = ("organization_name", "user", "status", "verified_by")
    list_filter = ("status", "verified_by")
    search_fields = ("organization_name", "user__username", "user__email")


# Event Admin
class EventAdmin(CommonAdmin):
    list_display = (
        "name",
        "organizer",
        "category",
        "location",
        "start_date_time",
        "end_date_time",
        "status",
        "capacity",
        "price",
    )
    list_filter = (
        "category",
        "location",
        "status",
        "start_date_time",
        "end_date_time",
        "organizer",
    )
    search_fields = ("name", "location", "organizer__organization_name")


# Ticket Admin
class TicketAdmin(CommonAdmin):
    list_display = ("name", "event", "ticket_type", "price", "quantity", "created_at")
    list_filter = ("event", "ticket_type", "created_at")
    search_fields = ("name", "event__name")


# Booking Admin
class BookingAdmin(CommonAdmin):
    list_display = (
        "user",
        "ticket",
        "quantity",
        "total_amount",
        "status",
        "payment_method",
        "created_at",
    )
    list_filter = ("ticket__event", "status", "payment_method", "created_at")
    search_fields = ("user__username", "ticket__event__name")


# Media Admin
class MediaAdmin(CommonAdmin):
    list_display = ("event", "media_type", "caption_eng", "caption_nep")
    list_filter = ("event", "media_type")
    search_fields = ("event__name",)


# AuditLog Admin
class AuditLogAdmin(CommonAdmin):
    list_display = ("admin", "action", "target_type", "target_id", "timestamp")
    list_filter = ("admin", "action", "target_type", "timestamp")
    search_fields = ("admin__username", "action", "target_type")


# Notification Admin
class NotificationAdmin(CommonAdmin):
    list_display = ("user", "event", "medium", "status", "created_at")
    list_filter = ("user", "event", "medium", "status", "created_at")
    search_fields = ("user__username", "event__name", "message")


# QRCode Admin
class QRCodeAdmin(CommonAdmin):
    list_display = ("booking",)
    list_filter = ("booking",)
    search_fields = ("booking__user__username",)


# EventAnalytics Admin
class EventAnalyticsAdmin(CommonAdmin):
    list_display = ("event", "user", "views", "clicks", "last_viewed_at")
    list_filter = ("event", "user")
    search_fields = ("event__name", "user__username")


# EventReview Admin
class EventReviewAdmin(CommonAdmin):
    list_display = ("event", "user", "rating", "created_at")
    list_filter = ("event", "user", "rating", "created_at")
    search_fields = ("event__name", "user__username")


# Register models with their respective admin classes
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(AuditLog, AuditLogAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(QRCode, QRCodeAdmin)
admin.site.register(EventAnalytics, EventAnalyticsAdmin)
admin.site.register(EventReview, EventReviewAdmin)
