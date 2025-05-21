from django.contrib import admin
from .models import *

admin.site.register(Organizer)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Booking)
admin.site.register(Media)
admin.site.register(AuditLog)
admin.site.register(Notification)
admin.site.register(QRCode)
admin.site.register(EventAnalytics)
admin.site.register(EventReview)
