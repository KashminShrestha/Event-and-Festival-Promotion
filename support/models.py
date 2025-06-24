from django.db import models

from django.conf import settings


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ("all", "All"),
        ("ticketing", "Ticketing"),
        ("payments", "Payments"),
        ("account_issue", "Account Issue"),
        ("organizer_help", "Organizer Help"),
    ]
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="all")

    def __str__(self):
        return self.question


class SupportRequest(models.Model):
    ISSUE_TYPE_CHOICES = [
        ("ticketing", "Ticketing"),
        ("payments", "Payments"),
        ("account_issue", "Account Issue"),
        ("organizer_help", "Organizer Help"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("closed", "Closed"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    issue_type = models.CharField(max_length=30, choices=ISSUE_TYPE_CHOICES)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="open"
    )  # open, closed, etc.
    priority_support = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_name} - {self.issue_type}"


class ContactInfo(models.Model):
    email_support = models.EmailField()
    phone_support = models.CharField(max_length=20)
    support_hour = models.CharField(max_length=100)  # e.g., "Mon-Fri 9am-6pm"
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email_support
