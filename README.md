# 🎉 Event and Festival Promotion Project

This repository contains the **backend** for an Event and Festival Promotion platform built with **Django**. It supports event management, ticketing, bookings, media uploads, notifications, and integrations with payment gateways like **Khalti** and **Firebase** for real-time features.

---

## 🚀 Features

- Organizer and Event management
- Ticket types and booking system
- Media uploads linked to events
- Notifications via SMS, Email, and Push
- Payment verification with **Khalti**
- Firebase integration for real-time database and messaging
- Audit logs and analytics

---

## 🛠 Getting Started

### ✅ Prerequisites

- Python 3.8+
- Django 5.x
- A Firebase project with credentials
- Khalti API keys
- Docker Desktop (for MailHog) for email testing / Mailtrap account for email testing

---

## 🚦 Feature : Organizer & Event Approval Workflow

🔍 Overview
This feature introduces a secure and structured approval system for both Organizers and Events, ensuring that only verified organizers and authorized events are available on the platform. It enhances trust, content quality, and platform transparency through audit logging and status control.

✅ Key Capabilities

1️⃣ Organizer Approval & Rejection

- Admin-Only Actions

  - Only admins have the authority to approve or reject organizer accounts.

- Status Tracking
  Each organizer has:

```bash
A status field: pending, approved, or rejected

A verified_by field to log the admin who took the action

Audit Logging
All actions are recorded in the AuditLog for accountability.

```

Example Endpoints:

```bash
POST /api/organizers/{id}/approve/   # Approves an organizer
POST /api/organizers/{id}/reject/    # Rejects an organizer
```

2️⃣ Event Approval, Rejection & Status Management

- Admin-Only Actions

  - Admins can approve, reject, or update the status of any event.

- Status Control

  - Events use a status field with values:

    - draft, published, cancelled

Audit Logging
Every status change is tracked for transparency.

Example Endpoints:

```bash
POST /api/events/{id}/approve/ — Publishes the event.
```

```bash
POST /api/events/{id}/reject/ — Cancels the event.
```

```bash
POST /api/events/{id}/change_status/ — Changes event status (e.g., from draft to published).
```

3️⃣ Permissions & Ownership

- Organizer Permissions

  - Only approved organizers can create and manage their events.

- Event Ownership Rules

  - Only the event's creator can update or delete it.

  - Edits and deletions are restricted to events in draft or cancelled status.

4️⃣ Multilingual Support

- 🗣️ Language Switching
  - The API supports multilingual content for event-related fields such as name and description.

#### ✅ Example Headers

| Key             | Value                   |
| --------------- | ----------------------- |
| Accept-Language | `en` or `ne`            |
| Authorization   | `Token YOUR_TOKEN_HERE` |
| Content-Type    | `application/json`      |

🧪 Example (cURL)

```bash
curl -H "Authorization: Token YOUR_TOKEN_HERE" \
     -H "Accept-Language: ne" \
     -H "Content-Type: application/json" \
     http://127.0.0.1:8000/api/events/5/
```

You can retrieve responses in either Nepali (ne) or English (en) by setting the Accept-Language header in your request.

Example API Usage
Approve an Organizer
text

```bash
POST /api/organizers/5/approve/
```

```bash
Authorization: Token <admin-token>
Response:

json
{
  "detail": "Organizer approved successfully."
}
Approve an Event
text
POST /api/events/10/approve/
Authorization: Token <admin-token>
Response:

json
{
  "detail": "Event approved and published."
}
```

Benefits
Quality Control: Ensures only vetted organizers and events are visible to users.

Accountability: Audit logs provide a trail of all admin actions.

Security: Strict permission checks prevent unauthorized actions.

Localization: Multilingual support enhances accessibility for diverse users.

Related Code Snippet
python

```bash
@action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
def approve(self, request, pk=None):
    organizer = self.get_object()
    if organizer.status == "approved":
        return Response({"detail": "Organizer already approved."}, status=400)
    organizer.status = "approved"
    organizer.verified_by = request.user
    organizer.save()
    AuditLog.objects.create(
        admin=request.user,
        action="Approved organizer",
        target_type="Organizer",
        target_id=organizer.id,
    )
    return Response({"detail": "Organizer approved successfully."}, status=200)
```

## 🧰 Utilities

This project includes several utility functions and modules to assist with common tasks such as:

- **Email Verification Utilities:** Functions to send and resend verification emails with OTPs for users and admins.
- **Notification Helpers:** Utilities for sending email, SMS and push notifications.
- **Payment Verification:** Helper functions to verify payments via Khalti API.

## 📚 Documentation Overview

- [📚 API Endpoints](docs/api_endpoints/README.md)  
  Detailed documentation of all available API endpoints, request/response formats, and examples.

- [🧰 Utilities](docs/utilities/UTILITIES.md)  
  Information about helper functions and utilities such as email verification, OTP handling, and notifications.

- [⚙️ Setup & Configuration](docs/setup.md)  
  Instructions for setting up the development environment, environment variables, and deployment.
