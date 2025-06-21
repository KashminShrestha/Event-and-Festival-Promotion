## 🧰 Utilities

This project includes several utility functions and modules to assist with common tasks such as:

- **Email Verification Utilities:** Functions to send and resend verification emails with OTPs for users and admins.
- **Notification Helpers:** Utilities for sending email, SMS and push notifications.
- **Payment Verification:** Helper functions to verify payments via Khalti API.

### How to Use Email Verification Utility

The email verification utilities are located in the `user/utils/email_verification.py` file.

You can import and use the `send_verification_email` and `resend_verification_email` functions in your views:

from user.utils.email_verification import send_verification_email, resend_verification_email

Example usage in a view
send_verification_email(request, user)

text

### Resend Verification Email Endpoint

We provide a reusable API endpoint to resend verification emails for both users and admins:

- **Endpoint:** `POST /user/resend-otp/resend-verification/`
- **Payload:**
  {
  "email": "user@example.com"
  }

text

- **Query Parameter:** Use `?admin=true` to resend for admin users.
