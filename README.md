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
- Mailtrap account for email testing

---

# 📦 Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/event-festival-promotion.git
```

```bash
cd event-festival-promotion
```

### Create and activate a virtual environment

```bash
python -m venv venv
```

```bash
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configure your environment variables (see below)

### Run migrations

```bash
python manage.py migrate
```

### Start the development server

```bash
python manage.py runserver
```

## Environment Variables Example (`.env`)

> 💡 **Tip:** Use a `.env` file to manage environment variables securely.

```bash
DEBUG=True

# ==============================
# 🔥 Firebase Configuration
# ==============================
FIREBASE_API_KEY="your-firebase-api-key"
FIREBASE_AUTH_DOMAIN="your-firebase-auth-domain"
FIREBASE_DATABASE_URL="your-firebase-db-url"
FIREBASE_PROJECT_ID="your-firebase-project-id"
FIREBASE_STORAGE_BUCKET="your-firebase-storage-bucket"
FIREBASE_MESSAGING_SENDER_ID="your-messaging-sender-id"
FIREBASE_APP_ID="your-firebase-app-id"
FIREBASE_MEASUREMENT_ID="your-measurement-id"
FIREBASE_CREDENTIAL_PATH="firebase_key.json"  # Path to your Firebase service account key

# ==============================
# 💳 Khalti Payment Gateway
# ==============================
KHALTI_VERIFY_URL="https://khalti.com/api/v2/payment/verify/"
KHALTI_PUBLIC_KEY="your-khalti-public-key"
KHALTI_SECRET_KEY="your-khalti-secret-key"

# ==============================
# 📧 Email Configuration (Mailtrap)
# ==============================
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="sandbox.smtp.mailtrap.io"
EMAIL_PORT=465
EMAIL_USE_TLS=True
EMAIL_HOST_USER="your-mailtrap-username"
EMAIL_HOST_PASSWORD="your-mailtrap-password"
DEFAULT_FROM_EMAIL="noreply@example.com"
```

> 📒 **Note:** Debug mode (True for development, False for production)
> & Replace all placeholder values with your actual credentials before running the project.

> ⚠️ **Warning:** This should not be pushed into git.

---

## 🚦 Feature 1: Organizer & Event Approval Workflow

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

### Summary Table

| Action        | Endpoint                          | Who Can Do It | Effect                        |
| ------------- | --------------------------------- | ------------- | ----------------------------- |
| is_approve    | `/user/staff-approval/approve/`   | Super Admin   | is_staff status → approved    |
| Approve Org   | `/api/organizers/{id}/approve/`   | Admin         | Organizer status → approved   |
| Reject Org    | `/api/organizers/{id}/reject/`    | Admin         | Organizer status → rejected   |
| Approve Event | `/api/events/{id}/approve/`       | Admin         | Event status → published      |
| Reject Event  | `/api/events/{id}/reject/`        | Admin         | Event status → cancelled      |
| Change Status | `/api/events/{id}/change_status/` | Admin         | Set event status (valid only) |

> 📒 **Note:** Check bash bellow for JSON request for is_staff approval (!! superuser action !!)

```bash
{
  "user_id": {id}
}
```

## 📚 API Summary

### 🛠️ Admin APIs

| Action                            | Method | Endpoint                           |
| --------------------------------- | ------ | ---------------------------------- |
| View All Analytics                | GET    | `/api/analytics/`                  |
| View Analytics for Specific Event | GET    | `/api/analytics/?event={event_id}` |
| View Audit Logs                   | GET    | `/api/auditlogs/`                  |

### 🔐 Authentication APIs

| Action             | Method | Endpoint                |
| ------------------ | ------ | ----------------------- |
| Admin Registration | POST   | `/user/admin/register/` |
| Admin Login        | POST   | `/user/admin/login/`    |
| OTP Verification   | POST   | `/user/verify-otp/`     |
| User Registration  | POST   | `/user/auth/users/`     |
| User Login         | POST   | `/auth/token/login/`    |
| OTP Verification   | POST   | `/user/verify-otp/`     |

> 📒 **Note:** OTP Verification
> Same for both Admin and User

### 🧑‍💼 Organizer APIs

| Action            | Method | Endpoint                        |
| ----------------- | ------ | ------------------------------- |
| Create Organizer  | POST   | `/api/organizers/`              |
| List Organizers   | GET    | `/api/organizers/`              |
| Approve Organizer | POST   | `/api/organizers/{id}/approve/` |
| Reject Organizer  | POST   | `/api/organizers/{id}/reject/`  |

### 🎉 Event APIs

| Action              | Method | Endpoint                          |
| ------------------- | ------ | --------------------------------- |
| Create Event        | POST   | `/api/events/`                    |
| List Events         | GET    | `/api/events/`                    |
| Update Event        | PATCH  | `/api/events/{id}/`               |
| Get Event by ID     | GET    | `/api/events/{id}/`               |
| Approve Event       | POST   | `/api/events/{id}/approve/`       |
| Reject Event        | POST   | `/api/events/{id}/reject/`        |
| Change Event Status | POST   | `/api/events/{id}/change_status/` |

### 🎟️ Ticket APIs

| Action        | Method | Endpoint        |
| ------------- | ------ | --------------- |
| Create Ticket | POST   | `/api/tickets/` |
| List Tickets  | GET    | `/api/tickets/` |

### 📝 Booking APIs

| Action               | Method | Endpoint                             |
| -------------------- | ------ | ------------------------------------ |
| Create Booking       | POST   | `/api/bookings/`                     |
| List Bookings        | GET    | `/api/bookings/`                     |
| Booking with Payment | POST   | `/api/bookings/create_with_payment/` |

### 🖼️ Media APIs

| Action             | Method | Endpoint                        |
| ------------------ | ------ | ------------------------------- |
| Upload Media       | POST   | `/api/media/`                   |
| List Media         | GET    | `/api/media/`                   |
| Get Media by ID    | GET    | `/api/media/{id}/`              |
| Get Media by Event | GET    | `/api/events/{event_id}/media/` |

### 🔔 Notification APIs

| Action              | Method | Endpoint              |
| ------------------- | ------ | --------------------- |
| Create Notification | POST   | `/api/notifications/` |
| List Notifications  | GET    | `/api/notifications/` |

### ⭐ Review APIs

| Action                | Method | Endpoint                         |
| --------------------- | ------ | -------------------------------- |
| Create Review         | POST   | `/api/reviews/`                  |
| List Reviews          | GET    | `/api/reviews/`                  |
| Get Reviews for Event | GET    | `/api/reviews/?event={event_id}` |

### 📊 Analytics APIs

| Action                | Method | Endpoint                          |
| --------------------- | ------ | --------------------------------- |
| Create Analytics      | POST   | `/api/analytics/`                 |
| List Analytics        | GET    | `/api/analytics/`                 |
| Increment Event View  | POST   | `/api/analytics/increment-view/`  |
| Increment Event Click | POST   | `/api/analytics/increment-click/` |
