from django.db import models
from django.conf import settings



class Organizer(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )
    ORGANIZATION_TYPE_CHOICES = (
        ("registered_company", "Registered Company"),
        ("non_profit_company", "Non-profit Company"),
        ("government_entity", "Government Entity"),
        ("educational_institution", "Educational Institution"),
        ("individual", "Individual/Solo Proprietor"),
    )

    organization_type = models.CharField(
        max_length=50, choices=ORGANIZATION_TYPE_CHOICES, default="individual"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    verification_document = models.ImageField(
        upload_to="organization/verification/document/", null=True, blank=True
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organizer_profile",
    )

    organization_name = models.CharField(max_length=255)

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_organizers",
    )

    role = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.organization_name


class Event(models.Model):
    CATEGORY_CHOICES = (
        ("music", "Music"),
        ("sports", "Sports"),
        ("tech", "Tech"),
        ("food", "Food"),
        ("art", "Art"),
    )

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
        ("cancelled", "Cancelled"),
    )

    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, related_name="events"
    )
    name = models.CharField(max_length=255)
    name_nep = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    description_nep = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=255)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):

    TICKET_TYPE_CHOICES = [
        ("VIP", "VIP"),
        ("GA", "General Admission"),
        ("STUDENT", "Student"),
        ("DISCOUNT", "Discount"),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    ticket_type = models.CharField(
        max_length=20, choices=TICKET_TYPE_CHOICES
    )  # New field for ticket type
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.name}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    ]
    PAYMENT_METHOD_CHOICES = [
        ("esewa", "Esewa"),
        ("khalti", "Khalti"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="booking"
    )
    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class Media(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
        ("map", "Map"),
        ("banner", "Banner"),
    ]

    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="media")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)  #
    caption_eng = models.TextField(blank=True, null=True)
    caption_nep = models.TextField(blank=True, null=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    file = models.FileField(
        upload_to="media_uploads/", blank=True, null=True
    )  # <-- For uploads
    url = models.URLField(blank=True, null=True)  # For external links

    def __str__(self):
        return f"{self.media_type} for {self.event.name}"


class AuditLog(models.Model):
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="audit_logs"
    )
    action = models.CharField(max_length=255)
    target_type = models.CharField(max_length=255)
    target_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.email} - {self.action} on {self.target_type}({self.target_id})"


class Notification(models.Model):
    MEDIUM_CHOICES = [
        ("sms", "SMS"),
        ("email", "Email"),
        ("push", "Push"),
    ]
    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notify"
    )
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    message = models.TextField()
    medium = models.CharField(max_length=10, choices=MEDIUM_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class QRCode(models.Model):
    booking = models.OneToOneField(
        "Booking", on_delete=models.CASCADE, db_column="booking_id"
    )
    qr_code = models.TextField()

    def __str__(self):
        return f"QRCode for Booking {self.booking.id}"


class EventAnalytics(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_analytics",
    )
    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    last_viewed_at = models.DateTimeField(null=True, blank=True)


class EventReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="review"
    )
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
