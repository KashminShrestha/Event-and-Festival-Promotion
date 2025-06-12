# Event and Festival Promotion Project

This repository contains the backend for an Event and Festival Promotion platform built with Django. It supports event management, ticketing, bookings, media uploads, notifications, and integrations with payment gateways like Khalti and Firebase for real-time features.

---

## Features

- Organizer and Event management
- Ticket types and booking system
- Media uploads linked to events
- Notifications via SMS, Email, and Push
- Payment verification with Khalti
- Firebase integration for realtime database and messaging
- Audit logs and analytics

---

## Getting Started

### Prerequisites

- Python 3.8+
- Django 5.x
- A Firebase project with credentials
- Khalti API keys
- Mailtrap account for email testing

### Installation

1. Clone the repository:
git clone https://github.com/yourusername/event-festival-promotion.git
cd event-festival-promotion


2. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate


3. Install dependencies:
pip install -r requirements.txt


4. Configure your environment variables (see example below).

5. Run migrations:
python manage.py migrate

6. Start the development server:
python manage.py runserver



---

## Environment Variables Example (`.env`)


# Debug mode (True for development, False for production)
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


> **Note:** Replace all placeholder values with your actual credentials before running the project.

---




## Feature 


[1]: Organizer and Event Approval Workflow
Overview
Feature 1 in your codebase is the robust approval workflow for both Organizers and Events. This workflow ensures that only verified organizers and approved events are available on the platform, adding a layer of trust and quality control.

Key Capabilities
1. Organizer Approval & Rejection
Admin-only Actions: Only admin users can approve or reject organizers.

Status Tracking: Organizers have a status field (pending, approved, rejected) and a verified_by field to track the admin who performed the action.

Audit Logging: Every approval or rejection is logged in the AuditLog for transparency.

Example Endpoints:

POST /api/organizers/{id}/approve/ — Approves an organizer.

POST /api/organizers/{id}/reject/ — Rejects an organizer.

2. Event Approval, Rejection, and Status Change
Admin-only Actions: Only admins can approve, reject, or change the status of events.

Status Field: Events have a status (draft, published, cancelled).

Audit Logging: Every change is recorded in the AuditLog.

Example Endpoints:

POST /api/events/{id}/approve/ — Publishes the event.

POST /api/events/{id}/reject/ — Cancels the event.

POST /api/events/{id}/change_status/ — Changes event status (e.g., from draft to published).

3. Permissions and Ownership
Organizer Permissions: Only approved organizers can create or manage their own events.

Event Ownership: Only the event owner (organizer) can update or delete their event, and only when the event is in draft or cancelled state.

4. Multilingual Support
Language Switching: Event names and descriptions can be returned in Nepali or English, depending on the Accept-Language header.

Example API Usage
Approve an Organizer
text
POST /api/organizers/5/approve/
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
Benefits
Quality Control: Ensures only vetted organizers and events are visible to users.

Accountability: Audit logs provide a trail of all admin actions.

Security: Strict permission checks prevent unauthorized actions.

Localization: Multilingual support enhances accessibility for diverse users.

Related Code Snippet
python
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
Summary Table
Action	Endpoint	Who Can Do It	Effect
Approve Org	/api/organizers/{id}/approve/	Admin	Organizer status → approved
Reject Org	/api/organizers/{id}/reject/	Admin	Organizer status → rejected
Approve Event	/api/events/{id}/approve/	Admin	Event status → published
Reject Event	/api/events/{id}/reject/	Admin	Event status → cancelled
Change Status	/api/events/{id}/change_status/	Admin	Set event status (valid only)
