### 🛠️ Admin APIs

| Action                            | Method | Endpoint                           |
| --------------------------------- | ------ | ---------------------------------- |
| View All Analytics                | GET    | `/api/analytics/`                  |
| View Analytics for Specific Event | GET    | `/api/analytics/?event={event_id}` |
| View Audit Logs                   | GET    | `/api/auditlogs/`                  |

### 🔐 Authentication APIs

| Action             | Method | Endpoint                                           |
| ------------------ | ------ | -------------------------------------------------- |
| Admin Registration | POST   | `/user/admin/register/`                            |
| Admin Login        | POST   | `/user/admin/login/`                               |
| Admin Resend OTP   | POST   | `/user/resend-otp/resend-verification/`            |
| OTP Verification   | POST   | `/user/verify-otp/`                                |
| Change Password    | POST   | `/user/auth/change-password/`                      |
| User Registration  | POST   | `/user/auth/users/`                                |
| User Login         | POST   | `/auth/token/login/`                               |
| User Resend OTP    | POST   | `/user/resend-otp/resend-verification/?admin=true` |
| OTP Verification   | POST   | `/user/verify-otp/`                                |

> 📒 **Note:** OTP Verification and Change password
> Same for both Admin and User and after resending OTP same endpoint can be used for
> OTP verification and similaryly for change Password

### ✳️For OTP and other Utilities

For detailed documentation on OTP and other utilities, see the [`/docs/utilities/UTILITIES.md`](/docs/utilities/UTILITIES.md) file.  
Or explore the source code in the [`/user/utils/`](/user/utils/) directory.

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

### Summary Table

| Action        | Endpoint                          | Who Can Do It | Effect                        |
| ------------- | --------------------------------- | ------------- | ----------------------------- |
| is_approve    | `/user/staff-approval/approve/`   | Super Admin   | is_staff status → approved    |
| Approve Org   | `/api/organizers/{id}/approve/`   | Admin         | Organizer status → approved   |
| Reject Org    | `/api/organizers/{id}/reject/`    | Admin         | Organizer status → rejected   |
| Approve Event | `/api/events/{id}/approve/`       | Admin         | Event status → published      |
| Reject Event  | `/api/events/{id}/reject/`        | Admin         | Event status → cancelled      |
| Change Status | `/api/events/{id}/change_status/` | Admin         | Set event status (valid only) |

## API Endpoints Overview

| **Category**     | **Action**          | **Method** | **Endpoint**                                       | **Request Body Example**                                                                                                                                 | **Auth Required** |
| ---------------- | ------------------- | ---------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| Organizer        | Create Organizer    | POST       | `/api/organizers/`                                 | `{ "organization_name": "Organizer1", "user": 8 }`                                                                                                       | Yes (Token)       |
| Organizer        | List Organizers     | GET        | `/api/organizers/`                                 | _(none)_                                                                                                                                                 | Yes (Token)       |
| Events           | Create Event        | POST       | `/api/events/`                                     | `{ "name": "Music Festival", "name_nep": "संगीत महोत्सव", "description": "A grand music event.", ... }`                                                  | Yes (Token)       |
| Events           | List Events         | GET        | `/api/events/`                                     | _(none)_                                                                                                                                                 | Yes (Token)       |
| Events           | Update Event        | PATCH      | `/api/events/1/`                                   | `{ "name": "Updated Dashain Celebration 2025", ... }`                                                                                                    | Yes (Token)       |
| Events           | Get Event           | GET        | `/api/events/1/`                                   | _(none)_                                                                                                                                                 | Yes (Token)       |
| Analytics        | Create Analytics    | POST       | `/api/analytics/`                                  | _(none)_                                                                                                                                                 | Yes (Token)       |
| Analytics        | List Analytics      | GET        | `/api/analytics/`                                  | _(none)_                                                                                                                                                 | Yes (Token)       |
| Notifications    | Create Notification | POST       | `/api/notifications/`                              | _(none)_                                                                                                                                                 | Yes (Token)       |
| Notifications    | List Notifications  | GET        | `/api/notifications/`                              | _(none)_                                                                                                                                                 | Yes (Token)       |
| Reviews          | Create Review       | POST       | `/api/reviews/`                                    | `{ "event": 1, "rating": 5, "comment": "Amazing event!" }`                                                                                               | Yes (Token)       |
| Reviews          | List Reviews        | GET        | `/api/reviews/`                                    | _(none)_                                                                                                                                                 | Yes (Token)       |
| Tickets          | Create Ticket       | POST       | `/api/tickets/`                                    | `{ "event": 1, "name": "Vip", "price": "100.00", "quantity": 10, "ticket_type": "VIP" }`                                                                 | Yes (Token)       |
| Tickets          | List Tickets        | GET        | `/api/tickets/`                                    | _(none)_                                                                                                                                                 | Yes (Token)       |
| QrCodes          | Create QR Code      | POST       | `/api/qrcodes/`                                    | _(none)_                                                                                                                                                 | Yes (Token)       |
| QrCodes          | List QR Codes       | GET        | `/api/qrcodes/`                                    | _(none)_                                                                                                                                                 | Yes (Token)       |
| Authentication   | User Registration   | POST       | `/user/auth/users/`                                | `{ "name": "John Doe", "email": "john@example.com", "password": "...", "re_password": "...", "phone_number": "+9779800000000", "country_code": "+977" }` | No                |
| Authentication   | User Resend OTP     | POST       | `/user/resend-otp/resend-verification/`            | `{ "email": "john1@example.com" }`                                                                                                                       | No                |
| Authentication   | User Login          | POST       | `/auth/token/login/`                               | `{ "email": "john@example.com", "password": "strongpassword123" }`                                                                                       | No                |
| Authentication   | Password Reset      | POST       | `/user/auth/change-password/`                      | `{ "old_password": "StrongPassword123!", "new_password": "new_secure_password", "re_new_password": "new_secure_password" }`                              | Yes (Token)       |
| Authentication   | OTP Verification    | POST       | `/user/verify-otp/`                                | `{ "email": "john6@example.com", "otp": "132088" }`                                                                                                      | No                |
| Authentication   | Admin Registration  | POST       | `/user/admin/register/`                            | `{ "name": "Admin User", "email": "admin2@example.com", ... }`                                                                                           | No                |
| Authentication   | Admin Login         | POST       | `/user/admin/login/`                               | `{ "email": "admin2@example.com", "password": "new_secure_password" }`                                                                                   | No                |
| Authentication   | Admin Resend OTP    | POST       | `/user/resend-otp/resend-verification/?admin=true` | `{ "email": "admin@example.com" }`                                                                                                                       | No                |
| Bookings         | Create Booking      | POST       | `/api/bookings/`                                   | `{ "user": 2, "ticket": 11, "quantity": 2, "payment_method": "khalti" }`                                                                                 | Yes (Token)       |
| Bookings         | List Bookings       | GET        | `/api/bookings/`                                   | _(none)_                                                                                                                                                 | Yes (Token)       |
| Media Management | Upload Media        | POST       | `/api/media/`                                      | _(file upload)_                                                                                                                                          | Yes (Token)       |

---

## Notes

- Replace placeholders like `/api/` and `/user/` with your actual API base path.
- For endpoints with `*(none)*` in the request body, no body is required.
- Use the appropriate HTTP method as specified.
- Include the `Authorization` header with a valid token for secured endpoints.
- For file uploads, use `multipart/form-data` content type.

---

> 📒 **Note:** Check bash bellow for JSON request for is_staff approval (!! superuser action !!)

```bash
{
  "user_id": {id}
}
```
